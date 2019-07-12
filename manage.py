from flask import Flask, render_template
from flask_socketio import SocketIO, send, emit, ConnectionRefusedError, Namespace
import rsa
import sys
import re
import base64

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
    send(message)


socketio.on_event('login', handle_login, namespace='/chat')


@socketio.on('login')
def handle_login(message):
    send(message)


@socketio.on('key')
def handle_key(message):
    (pubkey, privkey) = rsa.newkeys(512)
    pub = pubkey.save_pkcs1()
    cry_file = open('cry_file.txt', 'w+')
    pubfile = open('public.pem', 'w+')
    pubfile.write(pub.decode('utf-8'))
    cry_file.write(pub.decode('utf-8'))
    pubfile.close()
    print(pub.decode('utf-8'))
    emit('key', pub.decode('utf-8'))


if __name__ == '__main__':
    socketio.run(app)
