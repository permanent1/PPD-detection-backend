from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, Form

from app.http import deps
from app.http.deps import get_db
from app.models.record import Record
from app.schemas.record import RecordDetail, RecordCreate, RecordUpdate, RecordDetail_m

import websocket  # websocket-client (https://github.com/websocket-client/websocket-client)
import requests
import random
import logging
import uuid

from obs import ObsClient
import os

server_address = "u486816-ac4b-dad91b77.westc.gpuhub.com:8443"
server_style_image_path = "style.png"
server_sketch_image_path = "sketch.png"
client_id = str(uuid.uuid4())

# 设置 AK/SK
ak = os.getenv("AccessKeyID")
sk = os.getenv("SecretAccessKey")
server = "https://obs.cn-south-1.myhuaweicloud.com"
bucket_name = "artist-eyes"

# 创建 obsClient 实例
obsClient = ObsClient(access_key_id=ak, secret_access_key=sk, server=server)

router = APIRouter(
    prefix="/records"
)


# 将前端传来的图片上传到华为云的OBS存储桶中
@router.post("/obs", response_model=RecordDetail_m, dependencies=[Depends(get_db)])
async def upload_obs_image(
        image: UploadFile = File(...),   # 接收前端上传的文件
        username: str = Form(...),       # 接收表单中的用户名
        user_id: int = Form(...),        # 接收表单中的用户ID
    ):
    '''
    将前端传来的图片上传到华为云的OBS存储桶中
    '''
    
    if not image:
        return jsonify({"error": "No file provided"}), 400

    temp_dir = './tmp'
    os.makedirs(temp_dir, exist_ok=True)  # 创建目录，若不存在

    file_location = os.path.join(temp_dir, image.filename)

    # 获取上传的文件的内容
    file_location = f'./tmp/{image.filename}'  # 临时存储路径

    # 将文件保存到临时路径
    with open(file_location, 'wb') as buffer:
        buffer.write(await image.read())

    # logging.info(f'接收到图片并保存到: {file_location}')

    try:
        # 上传文件到 OBS
        object_key = f'ppd/user_upload/{username}/{image.filename}'  # 使用用户名作为路径的一部分
        resp = obsClient.putFile(bucket_name, object_key, file_location)
        if resp.status < 300:
            logging.info(f"文件上传OBS成功: {resp.body.objectUrl}")

            draft_url = resp.body.objectUrl
            # 数据库添加一条新的记录信息
            record = Record.create(
                user_id=user_id,
                image=draft_url
            )
            return record

    finally:
        # 删除临时文件
        if os.path.exists(file_location):
            os.remove(file_location)


# 连接计算服务返回检测结果
@router.get("/result", response_model=list[RecordDetail_m], dependencies=[Depends(get_db)])
def get_records(skip: int = 0):
    """
    TODO 连接计算服务返回检测结果，并更新数据库
    """


    
    return 


# 获取所有记录
@router.get("/", response_model=list[RecordDetail_m], dependencies=[Depends(get_db)])
def get_records(skip: int = 0):
    """
    获取所有记录列表
    """
    records = Record.select().offset(skip)
    return list(records)


# 根据 ID 获取单个记录信息
@router.get("/{record_id}", response_model=RecordDetail, dependencies=[Depends(get_db)])
def get_record(record_id: int):
    """
    根据记录 ID 获取信息
    """
    record = Record.get_or_none(Record.id == record_id)
    record_detail = RecordDetail(
        id=record.id,
        user_id=record.user_id.id,  # 保留 user_id 字段
        result=record.result,
        image=record.image,
        res_image=record.res_image,
        size=record.size,
        length=record.length,
        width=record.width
    )
    if not record:
        raise HTTPException(status_code=404, detail="记录未找到")
    return record_detail


# 根据用户 ID 获取所有记录信息
@router.get("/user/{user_id}", response_model=list[RecordDetail], dependencies=[Depends(get_db)])
def get_record(user_id: int):
    """
    根据用户 ID 获取信息
    """
    records = Record.select().where(Record.user_id == user_id)
    # 手动构建返回的字典列表
    record_details = []
    for record in records:
        record_detail = RecordDetail(
            id=record.id,
            user_id=record.user_id.id,  # 保留 user_id 字段
            result=record.result,
            image=record.image,
            res_image=record.res_image,
            size=record.size,
            length=record.length,
            width=record.width,
            created_at=record.created_at,
            updated_at=record.updated_at
        )
        record_details.append(record_detail)
    if not record_details:
        raise HTTPException(status_code=404, detail="记录未找到")
    return list(record_details)


# 创建一个新的记录
@router.post("/", response_model=RecordDetail_m, dependencies=[Depends(get_db)])
def create_record(request_data: RecordCreate):
    """
    创建一个新的记录
    """
    record = Record.create(
        user_id=request_data.user_id,
        result=request_data.result,
        image=request_data.image,
        res_image=request_data.res_image,
        size=request_data.size,
        length=request_data.length,
        width=request_data.width
    )
    return record


# 更新记录信息
@router.put("/{record_id}", response_model=RecordDetail_m, dependencies=[Depends(get_db)])
def update_record(record_id: int, request_data: RecordUpdate):
    """
    更新记录信息
    """
    record = Record.get_or_none(Record.id == record_id)
    if not record:
        raise HTTPException(status_code=404, detail="记录未找到")

    record.result = request_data.result or record.result
    record.image = request_data.image or record.image
    record.res_image = request_data.res_image or record.res_image
    record.size = request_data.size or record.size
    record.length = request_data.length or record.length
    record.width = request_data.width or record.width
    record.save()
    
    return record
