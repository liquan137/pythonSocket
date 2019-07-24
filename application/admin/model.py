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


class py_key(BaseModel):
    public_pen = TextField(help_text='公匙', collation="utf8_general_ci")
    private_pen = TextField(help_text='私匙', collation="utf8_general_ci")
    create_time = CharField(max_length=40, help_text='创建时间', collation="utf8_general_ci")
    update_time = CharField(max_length=40, help_text='修改时间', collation="utf8_general_ci")
    ip = CharField(max_length=40, help_text='登录IP地址', collation="utf8_general_ci")

db.create_tables([py_key])

