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


class py_admin_key(BaseModel):
    public_pen = TextField(help_text='公匙', collation="utf8_general_ci")
    private_pen = TextField(help_text='私匙', collation="utf8_general_ci")
    create_time = CharField(max_length=40, help_text='创建时间', collation="utf8_general_ci")
    update_time = CharField(max_length=40, help_text='修改时间', collation="utf8_general_ci")
    ip = CharField(max_length=40, help_text='登录IP地址', collation="utf8_general_ci")


class py_user(BaseModel):
    user = CharField(max_length=20, help_text='用户', collation="utf8_general_ci")
    password = CharField(max_length=400, help_text='密码', collation="utf8_general_ci")
    create_time = CharField(max_length=40, help_text='创建时间', collation="utf8_general_ci")
    login_time = CharField(max_length=40, help_text='登录时间', collation="utf8_general_ci")


class py_user_admin(BaseModel):
    user = CharField(max_length=20, help_text='用户ID', collation="utf8_general_ci")
    avatar = CharField(max_length=400, help_text='用户头像', collation="utf8_general_ci",
                       default="https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif?imageView2/1/w/80/h/80")
    introduction = CharField(max_length=400, help_text='用户简介', collation="utf8_general_ci")
    name = CharField(max_length=40, help_text='管理员头衔', collation="utf8_general_ci")
    roles = CharField(max_length=120, help_text='管理员级别', collation="utf8_general_ci")
    create_time = CharField(max_length=40, help_text='创建时间', collation="utf8_general_ci")
    update_time = CharField(max_length=40, help_text='修改时间', collation="utf8_general_ci")

db.create_tables([py_admin_key, py_user, py_user_admin])
# try:
#     py_user.get(py_user.user == '18027046690')
#     print('成功')
# except:
#     print('错误'+str(py_user.get(py_user.id == '1').user))
