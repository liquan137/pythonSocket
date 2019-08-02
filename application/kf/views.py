from . import kf
import time
from flask import jsonify, request
from . import model
from peewee import *
import requests
from pubg_python import PUBG, Shard
api = PUBG('eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiJmZDZlZDVmMC05MDA5LTAxMzctOTVkMC00N2ZiNGVlMjNhYjEiLCJpc3MiOiJnYW1lbG9ja2VyIiwiaWF0IjoxNTYzOTQ5NjMwLCJwdWIiOiJibHVlaG9sZSIsInRpdGxlIjoicHViZyIsImFwcCI6Ii1mZmY0MzgzNi04ZTU0LTQ1ZDktOTYyOC05YTZjOWVkN2RiMGIifQ.wRSBYFLGV_vxrI3pRoKN-i8XRg89pC9i4R0VJ1NAA7g', Shard.PC_NA)

# 创建客服新类型
@kf.route("/kf_type", methods=['PUT'])
def kf_type():
    type = request.values.get('type')
    if type != '':
        try:
            find = model.py_user_kf_type.get(model.py_user_kf_type.type == type)
            return jsonify({
                'code': 401,
                'message': '创建失败'
            })
        except:
            model.py_user_kf_type.create(type=type, create_time=time.time())
            return jsonify({
                'code': 200,
                'message': '创建成功'
            })
    else:
        return jsonify({
            'code': 401,
            'message': '客服类型命名不能为空'
        })


# 查询所有客服类型
@kf.route("/kf_type", methods=['POST'])
def kf_type_get():
    try:
        find = model.py_user_kf_type.select()
        index = 0
        list = []
        if len(find) > 0:
            while index < len(find):
                list.append({'name': find[index].type, 'create_time': time.strftime('%Y-%m-%d %H:%M', time.localtime(
                    float(find[index].create_time)))})
                index += 1
            return jsonify({
                'code': 200,
                'message': '查询成功',
                'data': list
            })
        else:
            return jsonify({
                'code': 200,
                'message': '没有数据',
                'data': []
            })
    except:
        return jsonify({
            'code': 401,
            'message': '查询失败'
        })


# 查询客服列表
@kf.route("/list", methods=['POST'])
def kf_list():
    start = request.values.get('start')
    length = request.values.get('length')
    type = request.values.get('type')
    name = request.values.get('name')
    timeRange = request.values.getlist('time[]')
    print(timeRange)

    if type == None and name == None:
        find = model.py_user_kf.select().order_by(model.py_user_kf.create_time.desc()).paginate(int(start),
                                                                                                int(
                                                                                                    length))
    else:
        find = model.py_user_kf.select().where((model.py_user_kf.type.contains(str(type))),
                                               (model.py_user_kf.name.contains(str(name))), ).order_by(
            model.py_user_kf.create_time.desc()).paginate(int(start),
                                                          int(
                                                              length))
    if len(timeRange) > 0:
        find = model.py_user_kf.select().where(
            (model.py_user_kf.type.contains(str(type))),
            (model.py_user_kf.name.contains(str(name))),
            (model.py_user_kf.login_time.between(timeRange[0], timeRange[1]))
        ).order_by(model.py_user_kf.create_time.desc()).paginate(int(start), int(length))
    else:
        print(find.sql())
    try:
        count = model.py_user_kf.select().count()

        index = 0
        list = []
        while index < len(find):
            list.append(
                {'id': find[index].id, 'num': find[index].num, 'name': find[index].name, 'type': find[index].type,
                 'user': find[index].user,
                 'login_time': time.strftime('%Y-%m-%d %H:%M', time.localtime(float(find[index].login_time))),
                 'create_time': time.strftime('%Y-%m-%d %H:%M', time.localtime(float(find[index].create_time))),
                 'update_time': time.strftime('%Y-%m-%d %H:%M', time.localtime(float(find[index].update_time)))})
            index += 1
        return jsonify({
            'code': 200,
            'message': '查询成功',
            'data': list,
            'total': count
        })
    except:
        return jsonify({
            'code': 401,
            'message': '查询失败'
        })


# 创建客服账号
@kf.route("/add", methods=['PUT'])
def create():
    id = request.values.get('id')
    name = request.values.get('name')
    type = request.values.get('type')
    # num = request.values.get('num')  客服编号不可修改，自动分配
    user = request.values.get('user')
    login_time = time.time()
    create_time = time.time()
    update_time = time.time()

    try:
        query = model.py_user_kf.select(fn.Max(model.py_user_kf.num)).scalar()
        print(query)
    except:
        num = 1000
    try:
        find = model.py_user_kf.create(name=name, type=type, num=query + 1, user=user, login_time=login_time,
                                       create_time=create_time,
                                       update_time=update_time)
        return jsonify({
            'code': 200,
            'message': '创建成功'
        })
    except:
        return jsonify({
            'code': 401,
            'message': '创建失败'
        })


# 创建客服账号
@kf.route("/update", methods=['PUT'])
def update():
    id = request.values.get('id')
    name = request.values.get('name')
    type = request.values.get('type')
    num = request.values.get('num')
    user = request.values.get('user')
    login_time = ''
    create_time = time.time()
    update_time = time.time()
    try:
        find = model.py_user_kf.get(model.py_user_kf.id == int(id))
        find.name = name
        find.user = user
        find.type = type
        # find.num = num 客服编号不可修改
        find.update_time = time.time()
        find.save()
        return jsonify({
            'code': 200,
            'message': '修改成功'
        })
    except:
        return jsonify({
            'code': 401,
            'message': '修改失败'
        })


# 删除客服
@kf.route("/delete", methods=['DELETE'])
def delete():
    id = request.values.get('id')
    try:
        find = model.py_user_kf.get(model.py_user_kf.id == int(id))
        find.delete_instance()
        return jsonify({
            'code': 200,
            'message': '删除成功'
        })
    except:
        return jsonify({
            'code': 401,
            'message': '删除失败'
        })

# 获取
@kf.route("/pubg", methods=['GET'])
def pubg():
    string = ''
    match = api.matches().get('64d3607b-8c28-4af1-a83d-d2e28a0dbe18')
    asset = match.assets[0]
    telemetry = api.telemetry(asset.url)
    player_kill_events = telemetry.events_from_type('LogPlayerKill')
    player_position_events = telemetry.events_from_type('LogPlayerPosition')
    print(player_kill_events)
    print(player_position_events)
    return '获取成功'

@kf.route("/pubg/player", methods=['GET'])
def player():
    name = request.values.get('name')
    if name == None:
        name = 'Angel_Wk'
    else:
        name = name
    print('姓名:'+str(name))
    players = api.players().filter(player_names=[str(name)])
    id = players[0]
    player = api.players().get(id)
    list = []
    html = ''
    head = '<tr><th>服务器</th><th>比赛时长</th><th>模式</th><th>被谁击杀</th><th>击杀你的玩家ID</th><th>行驶距离</th><th>存活时间</th><th>徒步距离</th><th>总伤害</th><th>击杀人数</th></tr>'
    index = 0
    for match in player.matches:
        game = api.matches().get(api.matches().get(match.id))
        participant = game.rosters[0].participants[0]
        print(participant)
        index += 1
        # list.append({
        #     'mode': game.game_mode,
        #     'duration': game.duration,
        #     'name': participant.name,
        #     'damage_dealt': participant.damage_dealt,
        #     'kills': participant.kills,
        #     'ride_distance': participant.ride_distance,
        #     'walk_distance': participant.walk_distance,
        #     'time_survived': participant.time_survived,
        #     'player_id': participant.player_id
        # })
        html += '<tr><th>服务器</th><th>'+str(game.duration)+'</th><th>'+str(game.game_mode)+'</th><th>'+str(participant.name)+'</th><th>'+str(participant.player_id)+'</th><th>'+str(participant.walk_distance)+'</th><th>'+str(participant.time_survived)+'</th><th>'+str(participant.walk_distance)+'</th><th>'+str(participant.damage_dealt)+'</th><th>'+str(participant.kills)+'</th></tr>'
    return '<table style="width:100%">'+head+html+'</table>'
