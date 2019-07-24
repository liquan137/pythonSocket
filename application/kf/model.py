from peewee import *
from application.config import config

sqlData = config.Data()
db = MySQLDatabase(
    host=sqlData['host'],
    user=sqlData['user'],
    password=sqlData['password'],
    database=sqlData['database'],
    charset="utf8"
)


class BaseModel(Model):
    class Meta:
        database = db

class py_user_kf(BaseModel):
    user = CharField(max_length=20, help_text='客服账号', collation="utf8_general_ci")
    password = CharField(max_length=400, help_text='客服密码', collation="utf8_general_ci", default='123456')
    name = CharField(max_length=100, help_text='客服名称', collation="utf8_general_ci")
    type = CharField(max_length=100, help_text='客服类型', collation="utf8_general_ci")
    avatar = CharField(max_length=400, help_text='客服头像', collation="utf8_general_ci",
                       default="https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif?imageView2/1/w/80/h/80")
    introduction = CharField(max_length=400, help_text='客服简介', collation="utf8_general_ci")
    num = IntegerField(help_text='客服编号', collation="utf8_general_ci")
    login_time = CharField(max_length=40, help_text='登录时间', collation="utf8_general_ci")
    create_time = CharField(max_length=40, help_text='创建时间', collation="utf8_general_ci")
    update_time = CharField(max_length=40, help_text='修改时间', collation="utf8_general_ci")

class py_user_kf_type(BaseModel):
    type = CharField(max_length=100, help_text='客服类型', collation="utf8_general_ci")
    create_time = CharField(max_length=40, help_text='创建时间', collation="utf8_general_ci")
db.create_tables([py_user_kf,py_user_kf_type])
