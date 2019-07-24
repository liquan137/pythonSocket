from flask import Flask, make_response
from .config import config
from flask_cors import CORS

app = Flask(__name__)
app.debug = True


@app.after_request
def af_request(resp):
    """
    #请求钩子，在所有的请求发生后执行，加入headers。
    :param resp:
    :return:
    """
    resp = make_response(resp)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Methods'] = 'POST, PUT, GET, DELETE, OPTIONS, HEAD'
    resp.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type,x-token'

    return resp


CORS(app, supports_credentials=True)
from .home import home as home_blueprint

app.register_blueprint(home_blueprint, url_prefix='/home')  # url_prefix是访问蓝图的链接前缀如：www.abc.com/admin

from .admin import admin as admin_blueprint

app.register_blueprint(admin_blueprint, url_prefix='/admin')  # url_prefix是访问蓝图的链接前缀如：www.abc.com/admin

from .user import user as user_blueprint

app.register_blueprint(user_blueprint, url_prefix='/user')  # url_prefix是访问蓝图的链接前缀如：www.abc.com/admin

from .kf import kf as kf_blueprint

app.register_blueprint(kf_blueprint, url_prefix='/kf')  # url_prefix是访问蓝图的链接前缀如：www.abc.com/admin

