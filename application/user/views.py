from . import user
from flask import jsonify, request
from Crypto import Random
from Crypto.PublicKey import RSA
import time
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
import base64
import json
import urllib.request
from . import model


@user.route("/key", methods=['POST'])
def key():
    ip = request.remote_addr
    RANDOM_GENERATOR = Random.new().read
    rsa = RSA.generate(1024, RANDOM_GENERATOR)
    PRIVATE_PEM = rsa.exportKey()
    PUBLIC_PEM = rsa.publickey().exportKey()
    try:
        find = model.py_admin_key.get(model.py_admin_key.ip == ip)
        if find.update_time + 1800 < time.time():
            find.public_pen = PUBLIC_PEM.decode("utf-8")
            find.private_pen = PRIVATE_PEM.decode("utf-8")
            find.update_time = time.time()
            find.save()
            return jsonify({'code': 20000, 'data': PUBLIC_PEM.decode("utf-8")})
        else:
            return jsonify({'code': 20000, 'data': find.public_pen})
    except:
        model.py_admin_key.create(ip=ip, public_pen=PUBLIC_PEM.decode("utf-8"),
                                  private_pen=PRIVATE_PEM.decode("utf-8"), update_time=time.time(),
                                  create_time=time.time())
        return jsonify({'code': 20000, 'data': PUBLIC_PEM.decode("utf-8")})


@user.route("/view", methods=['GET'])
def index():
    html = request.args.get('html')
    print(html)
    return str(html)


@user.route("/login", methods=['POST', 'GET'])
def login():
    ip = request.remote_addr
    if request.method == 'POST':
        data = request.json
        password = data['password']
        username = data['username']
        find = model.py_admin_key.get(model.py_admin_key.ip == ip)
        rsakey = RSA.importKey(find.private_pen)
        cipher = Cipher_pkcs1_v1_5.new(rsakey)
        random_generator = Random.new().read
        pwd = cipher.decrypt(base64.b64decode(password), None)
        pwd = pwd.decode('utf-8')
        print('解密后的密码：' + pwd)
        try:
            admin = model.py_user.get(model.py_user.user == username)
            if pwd == admin.password:
                return jsonify(
                    {'code': 20000, 'data': {'token': 'admin-token'}})
            else:
                return jsonify({
                    'code': 60204,
                    'message': '密码错误'
                })
        except:
            return jsonify({
                'code': 60204,
                'message': '账号或者密码错误'
            })
    else:
        return jsonify({
            'code': 60204,
            'message': '请求错误'
        })


@user.route("/info", methods=['GET'])
def info():
    if request.method == 'GET':
        return jsonify({'code': 20000, 'data': {
            'roles': ['admin'],
            'introduction': 'I am a super administrator',
            'avatar': 'https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif',
            'name': 'Super Admin'
        }})
    else:
        return jsonify({
            'code': 60204,
            'message': 'Account and password are incorrect.'
        })
