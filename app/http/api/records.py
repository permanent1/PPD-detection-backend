from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, Form
from fastapi.responses import JSONResponse

from app.http import deps
from app.http.deps import get_db
from app.models.record import Record
from app.schemas.record import RecordDetail, RecordCreate, RecordUpdate, RecordDetail_m

import websocket  # websocket-client (https://github.com/websocket-client/websocket-client)
import requests
import random
import logging
import uuid
import base64
from pathlib import Path

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
    prefix="/records"
)


# 将前端传来的图片上传到华为云的OBS存储桶中，并返回结果
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

    # 将文件读取为字节流形式
    image_bytes = await image.read()

    temp_dir = './tmp/input'
    os.makedirs(temp_dir, exist_ok=True)  # 创建目录，若不存在

    image_location = os.path.join(temp_dir, image.filename)

    # 将文件保存到临时路径
    with open(image_location, 'wb') as buffer:
        buffer.write(image_bytes)

    logging.info(f'接收到图片并保存到: {image_location}')

    # 获取当前时间并格式化为字符串，例如：'2024-05-19_12-45-30'
    current_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

    # 上传用户上传的文件到 OBS
    object_key = f'ppd/{username}/{current_time}/{image.filename}'  # 使用用户名作为路径的一部分
    resp1 = obsClient.putFile(bucket_name, object_key, image_location)

    # logging.info(f"用户文件上传OBS成功: {resp.body.objectUrl}")
    image_url = resp1.body.objectUrl

    # 获取检测结果
    response_json = detect_ppd(image.filename, image_bytes, image.content_type)
    res_image_location = response_json["res_image_location"]
    result = response_json["result"]
    width = response_json["width"]
    length = response_json["length"]
    size = response_json["size"]
    result_text = response_json["result_text"]
    time = response_json["time"]

    # 上传检测结果文件到 OBS
    object_key = f'ppd/{username}/{current_time}/result_{image.filename}'  # 使用用户名作为路径的一部分
    resp2 = obsClient.putFile(bucket_name, object_key, res_image_location)

    # logging.info(f"检测文件上传OBS成功: {resp.body.objectUrl}")
    res_image_url = resp2.body.objectUrl


    # 向数据库中新添加一个记录
    record = Record.create(
        user_id=user_id,
        image=image_url,
        res_image=res_image_url,
        result=result,
        width=width,
        length=length,
        size=size,
        description="待补充"
    )
    return record


def detect_ppd(filename, image_bytes, content_type):

    # 将图片上传到PPD算法模型端获取检测结果
    files = [
        ('image', (filename, image_bytes, content_type))
    ]

    response = requests.post(remote_url, files=files)
    # response_json = response.json()
    # return response_json
    if response.status_code == 200:
        response_json = response.json()
        result_image = response_json["result_image"]
        result_text = response_json["result_text"]
        result_info = response_json["result_info"]
        time = response_json["time"]

        # 解码 base64 字符串为二进制数据
        result_image_data = base64.b64decode(result_image)
        # 保存图片到本地
        output_dir = Path('tmp/result')  # 输出目录
        output_dir.mkdir(parents=True, exist_ok=True)  # 确保目录存在
        output_file = output_dir / f"{filename}_result.png"  # 输出文件路径

        with open(output_file, "wb") as f:
            f.write(result_image_data)

        # # 删除临时文件
        # if os.path.exists(file_location):
        #     os.remove(file_location)

        return {
            "res_image_location": output_file,
            "result": result_info["result"],
            "width": result_info["width"],
            "length": result_info["length"],
            "size": result_info["size"],
            "result_text":result_text,
            "time":time
        }
    else:
        raise HTTPException(status_code=500, detail="算法服务请求失败")


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
        description=record.description,
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
            description=record.description,
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
