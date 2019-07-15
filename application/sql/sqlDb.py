import sqlobject
from sqlobject.mysql import builder

conn = builder()(user='root', password='root', host='localhost', db='test')


class py_user(sqlobject.SQLObject):
    try:
        _connection = conn
        user = sqlobject.StringCol(length=14, unique=True)
        password = sqlobject.StringCol(length=255)
        create_time = sqlobject.StringCol(length=255)
        login_time = sqlobject.StringCol(length=255)
    except:
        print("创建py_user失败")
    else:
        print("创建py_user成功")


class py_key(sqlobject.SQLObject):
    try:
        _connection = conn
        public_pen = sqlobject.StringCol(length=500)
        private_pen = sqlobject.StringCol(length=500)
        create_time = sqlobject.StringCol(length=500)
        update_time = sqlobject.StringCol(length=500)
        ip = sqlobject.StringCol(length=500)
    except:
        print("创建py_key失败")
    else:
        print("创建py_key成功")


def start():
    print("链接数据库")
    py_user.createTable(ifNotExists=True)
    py_key.createTable(ifNotExists=True)
