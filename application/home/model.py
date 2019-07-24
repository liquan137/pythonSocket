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


class py_rule(BaseModel):
    title = CharField(max_length=40, help_text='分类名称', collation="utf8_general_ci")
    user = CharField(max_length=40, help_text='绑定用户', collation="utf8_general_ci")
    create_time = CharField(max_length=40, help_text='创建时间', collation="utf8_general_ci")
    update_time = CharField(max_length=40, help_text='修改时间', collation="utf8_general_ci")

class py_rule_reply(BaseModel):
    rule_id = CharField(max_length=40, help_text='关联总规则的id', collation="utf8_general_ci")
    title = CharField(max_length=40, help_text='子规则名称', collation="utf8_general_ci")
    user = CharField(max_length=40, help_text='用户id', collation="utf8_general_ci")
    touch = CharField(max_length=120, help_text='触发条件', collation="utf8_general_ci")
    reply = CharField(max_length=2000, help_text='回复内容', collation="utf8_general_ci")
    create_time = CharField(max_length=40, help_text='创建时间', collation="utf8_general_ci")
    update_time = CharField(max_length=40, help_text='修改时间', collation="utf8_general_ci")

class py_rule_type(BaseModel):
    type_id = CharField(max_length=40, help_text='关联分类的id', collation="utf8_general_ci")
    title = CharField(max_length=40, help_text='规则名称', collation="utf8_general_ci")
    user = CharField(max_length=40, help_text='用户id', collation="utf8_general_ci")
    create_time = CharField(max_length=40, help_text='创建时间', collation="utf8_general_ci")
    update_time = CharField(max_length=40, help_text='修改时间', collation="utf8_general_ci")


db.create_tables([py_rule, py_rule_reply, py_rule_type])
