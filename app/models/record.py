from peewee import CharField, ForeignKeyField, IntegerField, DoubleField
from app.models.base_model import BaseModel
from app.models.user import User  # User 模型在 user.py 中

class Record(BaseModel):
    class Meta:
        table_name = 'records'

    id = IntegerField(primary_key=True)
    user_id = ForeignKeyField(User, backref='users', on_delete='CASCADE', on_update='CASCADE', help_text="用户外键")
    result = CharField(null=True, max_length=255, help_text="检测结果 阴性/阳性")
    image = CharField(null=True, max_length=255, help_text="用户上传图片路径")
    res_image = CharField(null=True, max_length=255, help_text="检测结果图片路径")
    size = DoubleField(null=True, help_text="红肿大小")
    length = DoubleField(null=True, help_text="长度")
    width = DoubleField(null=True, help_text="宽度")
    description = CharField(null=True, max_length=255, help_text="描述")

    def __str__(self):
        return f'Artwork: {self.artwork} by {self.artist_id.name}'

    def has_image(self):
        return bool(self.url)
