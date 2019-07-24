import sqlobject
from sqlobject.mysql import builder

conn = builder()(user='root', password='root', host='localhost', db='test', charset="utf8")


# class py_user(sqlobject.SQLObject):
#     _connection = conn
#     user = sqlobject.StringCol(length=14, unique=True)
#     password = sqlobject.StringCol(length=255)
#     create_time = sqlobject.StringCol(length=255)
#     login_time = sqlobject.StringCol(length=255)
#     # print("创建py_user成功")
#
#
# class py_key(sqlobject.SQLObject):
#     _connection = conn
#     public_pen = sqlobject.StringCol(length=500)
#     private_pen = sqlobject.StringCol(length=500)
#     create_time = sqlobject.StringCol(length=500)
#     update_time = sqlobject.StringCol(length=500)
#     ip = sqlobject.StringCol(length=500)
#     # print("创建py_key成功")
#
#
# class py_rule(sqlobject.SQLObject):
#     _connection = conn
#     title = sqlobject.StringCol(length=500)
#     user = sqlobject.StringCol(length=500)
#     create_time = sqlobject.StringCol(length=500)
#     update_time = sqlobject.StringCol(length=500)
#     # print("创建py_rule成功")
#
#
# class py_rule_reply(sqlobject.SQLObject):
#     _connection = conn
#     rule_id = sqlobject.StringCol(length=100)
#     title = sqlobject.StringCol(length=500)
#     user = sqlobject.StringCol(length=500)
#     touch = sqlobject.StringCol(length=500)
#     reply = sqlobject.StringCol(length=500)
#     create_time = sqlobject.StringCol(length=500)
#     update_time = sqlobject.StringCol(length=500)
#     # print("创建py_rule_reply成功")
#

def start():
    print("")
    # py_user.createTable(ifNotExists=True)
    # py_key.createTable(ifNotExists=True)
    # py_rule.createTable(ifNotExists=True)
    # py_rule_reply.createTable(ifNotExists=True)
