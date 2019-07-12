import pymysql
import pymysql.cursors
import json


def connectdb():
    print('连接到mysql服务器...')
    # 打开数据库连接
    # 用户名:hp, 密码:Hp12345.,用户名和密码需要改成你自己的mysql用户名和密码，并且要创建数据库TESTDB，并在TESTDB数据库中创建好表Student
    db = pymysql.connect("localhost", "root", "root", "test")
    print('连接上了!')
    return db


def closedb(db):
    db.close()
    print('链接关闭了')


def find(db, sql):
    cursor = db.cursor(cursor=pymysql.cursors.DictCursor)
    try:
        # 执行sql语句
        cursor.execute(sql)
        results = cursor.fetchall()
        print(json.dumps(results))
    except:
        # Rollback in case there is any error
        print('查询数据失败!')
