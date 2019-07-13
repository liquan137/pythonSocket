from flask import Flask, render_template, request
from flask_socketio import SocketIO, send, emit, ConnectionRefusedError, Namespace
import sys
from Crypto import Random
import json
from Crypto.PublicKey import RSA
import time
from application.config import config
from application.sql import db

print(sys.version)
print(sys.getdefaultencoding())
print(sys.getfilesystemencoding())

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)


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
    emit('msg', json.dumps({'type': 'success', 'msg': '登录成功'}, ensure_ascii=False))
    print(json.dumps(message, ensure_ascii=False))


@socketio.on('key')
def handle_key(message):
    RANDOM_GENERATOR = Random.new().read
    rsa = RSA.generate(1024, RANDOM_GENERATOR)
    # master的秘钥对的生成
    PRIVATE_PEM = rsa.exportKey()
    # with open('master-private.pem', 'w') as f:
    #     f.write(PRIVATE_PEM.decode('utf-8'))
    # print
    # PRIVATE_PEM
    PUBLIC_PEM = rsa.publickey().exportKey()
    print
    # PUBLIC_PEM
    # with open('master-public.pem', 'w') as f:
    #     f.write(PUBLIC_PEM.decode('utf-8'))
    ip = request.remote_addr
    con = db.connectdb()
    keyFind = db.find(con, "SELECT * FROM  `py_key` WHERE  `ip` =  " + "'" + ip + "'")
    if keyFind == 'None':
        print('创建密匙')
        db.insert(con, 'py_key',
                  [{'public_pen': PUBLIC_PEM.decode('utf-8'), 'private_pen': PRIVATE_PEM.decode('utf-8'),
                    'create_time': time.time(), 'ip': ip}])
    else:
        db.update(con, 'py_key', [{'public_pen': PUBLIC_PEM.decode('utf-8'), 'private_pen': PRIVATE_PEM.decode('utf-8'),
                                   'create_time': time.time()}], {'ip': ip, 'id': 27})
        print('更新密匙')

    db.closedb(con)
    emit('key', PUBLIC_PEM.decode('utf-8'))




if __name__ == '__main__':
    socketio.run(app)
