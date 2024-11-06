from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, Form

from app.http import deps
from app.http.deps import get_db
from app.models.user import User
from app.schemas.user import UserDetail,UserCreate,UserUpdate
from app.services.auth import hashing

import logging
from datetime import datetime

from obs import ObsClient
import os

# 设置计算服务远程参数
remote_url = "http://127.0.0.1:5000/detect/image"

# 设置 OBS访问 AK/SK
ak = os.getenv("AccessKeyID")
sk = os.getenv("SecretAccessKey")
server = "https://obs.cn-south-1.myhuaweicloud.com"
bucket_name = "artist-eyes"

# 创建 obsClient 实例
obsClient = ObsClient(access_key_id=ak, secret_access_key=sk, server=server)

router = APIRouter(
    prefix="/users"
)


@router.get("/me", response_model=UserDetail, dependencies=[Depends(get_db)])
def me(auth_user: User = Depends(deps.get_auth_user)):
    """
    当前登录用户信息
    """
    return auth_user


# 获取所有用户
@router.get("/", response_model=list[UserDetail], dependencies=[Depends(get_db)])
def get_users(skip: int = 0, limit: int = 10):
    """
    获取所有用户列表
    """
    users = User.select().offset(skip).limit(limit)
    return list(users)


# 根据 ID 获取单个用户信息
@router.get("/{user_id}", response_model=UserDetail, dependencies=[Depends(get_db)])
def get_user(user_id: int):
    """
    根据用户 ID 获取用户信息
    """
    user = User.get_or_none(User.id == user_id)
    if not user:
        raise HTTPException(status_code=404, detail="用户未找到")
    return user


# 更新用户信息
@router.post("/{user_id}", response_model=UserDetail, dependencies=[Depends(get_db)])
def update_user(user_id: int, user_update: UserUpdate):
    """
    根据用户 ID 更新用户信息
    """
    user = User.get_or_none(User.id == user_id)
    if not user:
        raise HTTPException(status_code=404, detail="用户未找到")

    # 更新用户信息
    user_data = user_update.dict(exclude_unset=True)  # 仅更新提供的字段
    for key, value in user_data.items():
        setattr(user, key, value)

    # 保存到数据库
    user.save()

    return user


# 上传头像到obs
@router.post("/avatar/obs", response_model=UserDetail, dependencies=[Depends(get_db)])
async def upload_obs_image(
        image: UploadFile = File(...),   # 接收前端上传的文件
        user_id: int = Form(...),        # 接收表单中的用户ID
    ):
    '''
    将前端传来的头像图片上传到华为云的OBS存储桶中
    '''
    
    if not image:
        return jsonify({"error": "No file provided"}), 400

    # 将文件读取为字节流形式
    image_bytes = await image.read()

    temp_dir = './tmp/avatar'
    os.makedirs(temp_dir, exist_ok=True)  # 创建目录，若不存在

    image_location = os.path.join(temp_dir, image.filename)

    # 将文件保存到临时路径
    with open(image_location, 'wb') as buffer:
        buffer.write(image_bytes)

    logging.info(f'接收到用户头像图片并保存到: {image_location}')

    # 获取当前时间并格式化为字符串，例如：'2024-05-19_12-45-30'
    current_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

    # 上传用户上传的文件到 OBS
    object_key = f'ppd/avatar/{user_id}/avatar_{current_time}.png'  # 使用用户名作为路径的一部分
    resp = obsClient.putFile(bucket_name, object_key, image_location)

    # logging.info(f"用户文件上传OBS成功: {resp.body.objectUrl}")
    image_url = resp.body.objectUrl

    # 更新用户信息
    user = User.get_or_none(User.id == user_id)
    if not user:
        raise HTTPException(status_code=404, detail="用户未找到")
    
    user.avatar = image_url

    # 保存到数据库
    user.save()

    # 删除临时文件，如果想测试可以删除这两行代码，生成的结果就会存放在tmp目录下
    # 删除用户上传的图片
    if os.path.exists(image_location):
        os.remove(image_location)

    return user