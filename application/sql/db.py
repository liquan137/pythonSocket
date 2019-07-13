import pymysql
import pymysql.cursors
import json
import hashlib


def connectdb():
    print('连接到mysql服务器...')
    # 打开数据库连接
    db = pymysql.connect("localhost", "root", "root", "test")
    print('连接上了!')
    return db


def closedb(db):
    db.close()
    print('链接关闭了')


# 查询指定的一条数据
# db 当前链接的数据库
# sql 查询命令
def find(db, sql):
    cursor = db.cursor(cursor=pymysql.cursors.DictCursor)
    try:
        # 执行sql语句
        cursor.execute(sql)
        results = cursor.fetchall()
        print(json.dumps(results))
        if len(results) <= 0:
            return 'None'
        else:
            return results
    except:
        # Rollback in case there is any error
        print('查询数据失败!')
        return 'None'


# 指定数据表，新建表数据 此函数会循环嵌套着字典的列表，然后拼接成mysql命令然后执行
# db 当前链接的数据库
# table 指定的数据表
# arr 列表嵌套字典
def insert(db, table, arr):
    index = 0
    insertVal = []
    insertKeString = ''
    cursor = db.cursor()
    while index < len(arr):
        item = 0
        for key in arr[index]:
            insertVal.append(str(arr[index][key]).replace("\n", ""))
            if item == len(arr[index]) - 1:
                insertKeString += '`' + str(key) + '`'
                insertVal = tuple(insertVal)
                string = '(' + insertKeString + ')'
                sqlStr = "INSERT INTO `" + table + "` " + string + " VALUES " + str(
                    insertVal) + ';'
                print(sqlStr)
                cursor.execute(sqlStr)
                # 提交到数据库执行
                db.commit()
                print("遍历完成")
            else:
                insertKeString += '`' + str(key) + '`' + ', '
                print('仍在遍历中' + str(len(arr[index])))
                print(item)
            item += 1
        index += 1


# 更新指定数据表，精准指定更新
# db 当前链接的数据库
# table 指定的数据表
# arr 列表嵌套字典
# where 指定搜索的字段条件
def update(db, table, arr, where):
    index = 0
    updateStr = ''
    cursor = db.cursor()
    whereStr = ''
    time = 0
    for k in where:
        print(str(k) + ':' + str(where[k]))
        if time == len(where) - 1:
            whereStr += '`' + str(k) + '`' + '=' + "'" + str(where[k]) + "'"
        else:
            whereStr += '`' + str(k) + '`' + '=' + "'" + str(where[k]) + "'" + 'and'
        time += 1
    while index < len(arr):
        item = 0
        for key in arr[index]:
            if item == len(arr[index]) - 1:
                updateStr += '`' + str(key) + '` = ' + "'" + str(arr[index][key]) + "'"
                string = updateStr
                sqlStr = "UPDATE  `" + table + "` SET  " + string + " WHERE `" + table + "`." + whereStr + ";"
                print(sqlStr)
                cursor.execute(sqlStr)
                # 提交到数据库执行
                db.commit()
                print("遍历完成")
            else:
                updateStr += '`' + str(key) + '` = ' + "'" + str(arr[index][key]) + "'" + ','
                print('仍在遍历中' + str(len(arr[index])))
                print(item)
            item += 1
        index += 1
