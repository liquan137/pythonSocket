from flask import Flask, render_template, request
from flask_socketio import SocketIO, send, emit, ConnectionRefusedError, Namespace
import sys
from Crypto import Random
import json
from Crypto.PublicKey import RSA
import time
from application import app
from application.sql import sqlDb
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
import base64

print(sys.version)
print(sys.getdefaultencoding())
print(sys.getfilesystemencoding())

app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

print("开始创建数据表")
sqlDb.start()


@socketio.on('connect')
def test_connect():
    emit('my response', {'data': 'Connected'})
    print('Client connect')


@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')


@socketio.on('message')
def handle_message(message):
    print('received login: ' + str(message))


def handle_key(message):
    print('received key:' + str(message))


socketio.on_event('key', handle_key, namespace='/chat')


def handle_login(message):
    print('received login: ' + str(message))


socketio.on_event('login', handle_login, namespace='/chat')


@socketio.on('login')
def handle_login(message):
    print(json.dumps(message, ensure_ascii=False))
    keyFind = sqlDb.py_key.select(sqlDb.py_key.q.ip == str(request.remote_addr))[0]
    password = message['pwd']
    rsakey = RSA.importKey(keyFind.private_pen)
    cipher = Cipher_pkcs1_v1_5.new(rsakey)
    random_generator = Random.new().read
    pwd = cipher.decrypt(base64.b64decode(password), None)
    pwd = pwd.decode('utf-8')
    userFind = sqlDb.py_user.select(sqlDb.py_user.q.user == message['user'])
    print(len(list(userFind)))
    if len(list(userFind)) > 0:
        if userFind[0].password == pwd:
            emit('msg', json.dumps({'type': 'success', 'msg': '登录成功', 'states': '1000'}, ensure_ascii=False))
        else:
            emit('msg', json.dumps({'type': 'success', 'msg': '账号或密码错误', 'states': '1001'}, ensure_ascii=False))
    else:
        emit('msg', json.dumps({'type': 'success', 'msg': '没有此账号', 'states': '1002'}, ensure_ascii=False))


@socketio.on('key')
def handle_key(message):
    RANDOM_GENERATOR = Random.new().read
    rsa = RSA.generate(1024, RANDOM_GENERATOR)
    # 秘钥对的生成
    PRIVATE_PEM = rsa.exportKey()
    PUBLIC_PEM = rsa.publickey().exportKey()
    print(PRIVATE_PEM.decode('utf-8'))
    ip = request.remote_addr
    keyFind = sqlDb.py_key.select(sqlDb.py_key.q.ip == str(ip))
    if len(list(keyFind)) == 0:
        print('创建密匙')
        sqlDb.py_key(public_pen=PUBLIC_PEM.decode('utf-8'), private_pen=PRIVATE_PEM.decode('utf-8'),
                     create_time=str(time.time()), ip=str(ip), update_time='')
        emit('key', PUBLIC_PEM.decode('utf-8'))
    else:
        keyFind[0].public_pen = str(PUBLIC_PEM.decode('utf-8'))
        keyFind[0].private_pen = str(PRIVATE_PEM.decode('utf-8'))
        keyFind[0].update_time = str(time.time())
        print('更新密匙:' + str(keyFind))
        emit('key', PUBLIC_PEM.decode('utf-8'))


if __name__ == '__main__':
    socketio.run(app)
