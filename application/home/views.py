from . import home
from flask import jsonify, request
from . import model
import time
import json
import urllib.request


@home.route("/rule", methods=['POST'])
def index():
    print(request.headers['X-Token'])
    if request.method == 'POST':
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


# 创建大分类
@home.route("/add", methods=['PUT', 'POST'])
def ruleSet():
    data = request.json
    title = data.get('title')
    print(type(title))
    user = data.get('user')
    try:
        num = model.py_rule.get(model.py_rule.title == title)
        return jsonify({
            'code': 400,
            'message': '该分类已存在'
        })
    except:
        try:
            model.py_rule.create(title=title, user='', update_time=time.time(), create_time=time.time())
            return jsonify({
                'code': 200,
                'message': '分类创建成功'
            })
        except:
            return jsonify({
                'code': 401,
                'message': '创建失败'
            })


# 创建规则分类
@home.route("/rule_type", methods=['PUT'])
def ruleType():
    title = request.values.get('title')
    user = request.values.get('user')
    type_id = request.values.get('type_id')
    try:
        num = model.py_rule_type.get(model.py_rule_type.title == title, model.py_rule_type.type_id == type_id)
        return jsonify({
            'code': 400,
            'message': '该规则分类已存在'
        })
    except:
        try:
            model.py_rule_type.create(title=title, user='', update_time=time.time(), create_time=time.time(),
                                      type_id=type_id)
            return jsonify({
                'code': 200,
                'message': '规则类别创建成功'
            })
        except:
            return jsonify({
                'code': 401,
                'message': '创建失败'
            })


# 查询大分类及规则分类
@home.route("/rule", methods=['GET'])
def topRule():
    index = 0
    list = model.py_rule.select()
    if list.count() == 0:
        return jsonify({
            'code': 403,
            'message': '没有数据'
        })
    else:
        result = []
        while index < len(list):
            itemIndex = 0
            item = []
            try:
                find = model.py_rule_type.select().where(model.py_rule_type.type_id == list[index].id)
                while itemIndex < len(find):
                    item.append({'title': find[itemIndex].title, 'id': find[itemIndex].id})
                    itemIndex += 1
            except:
                item = []
            result.append({'id': list[index].id, 'title': list[index].title, 'list': item})
            index += 1
        return jsonify({
            'code': 200,
            'message': '查询成功',
            'data': result
        })


# 查询子规则列表
@home.route("/rule/detail", methods=['POST'])
def rule_detail():
    id = request.values.get('id')
    print(id)
    index = 0
    item = []
    try:
        find = model.py_rule_reply.select().where(model.py_rule_reply.rule_id == id)
        while index < len(find):
            item.append({'title': find[index].title, 'id': find[index].id, 'reply': find[index].reply,
                         'touch': (find[index].touch).split(','), 'rule_id': find[index].rule_id})
            index += 1
        return jsonify({
            'code': 200,
            'message': '查询成功',
            'data': item
        })
    except:
        return jsonify({
            'code': 403,
            'message': '没有数据',
            'data': []

        })


# 创建子规则
@home.route("/ruleChild", methods=['PUT', 'POST'])
def ruleChild():
    id = request.values.get('id')
    rule_id = request.values.get('rule_id')
    title = request.values.get('title')
    touch = request.values.getlist('touch[]')
    reply = request.values.get('reply')
    if request.method == 'PUT':
        if rule_id == '':
            return jsonify({
                'code': 402,
                'message': '请选择规则分类，再创建',
                'data': ''
            })
        else:
            String = ''
            index = 0
            while index < len(touch):
                if index + 1 == len(touch):
                    String += str(touch[index])
                else:
                    String += str(touch[index]) + ','
                index += 1
            touch = String
            try:
                find = model.py_rule_reply.get(model.py_rule_reply.title == title,
                                               model.py_rule_reply.rule_id == rule_id)
                index = 0
                return jsonify({
                    'code': 402,
                    'message': '规则：' + str(title) + '已经存在',
                    'data': ''
                })
            except:
                model.py_rule_reply.create(rule_id=rule_id, touch=touch, title=title, user='', reply=reply,
                                           update_time='',
                                           create_time=time.time())
                return jsonify({
                    'code': 200,
                    'message': '创建成功',
                    'data': rule_id
                })
    else:
        print(str(title) + ',' + str(id))
        try:
            find = model.py_rule_reply.get(model.py_rule_reply.title == title, model.py_rule_reply.id == id)
            String = ''
            index = 0
            while index < len(touch):
                if index + 1 == len(touch):
                    String += str(touch[index])
                else:
                    String += str(touch[index]) + ','
                index += 1
            touch = String
            find.touch = touch
            find.reply = reply
            find.update_time = time.time()
            find.save()
            return jsonify({
                'code': 200,
                'message': '修改成功',
            })
        except:
            return jsonify({
                'code': 402,
                'message': '修改失败',
                'data': ''
            })


@home.route("/rule/type", methods=['DELETE'])
def delete_type():
    id = request.values.get('id')
    try:
        find = model.py_rule_reply.get(model.py_rule_reply.id == id)
        find.delete_instance()
        return jsonify({
            'code': 200,
            'message': '删除成功',
        })
    except:
        return jsonify({
            'code': 402,
            'message': '删除失败',
            'data': ''
        })
