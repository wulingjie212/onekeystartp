# -*- coding: utf-8 -*-

from common.mymako import render_mako_context,render_json
from home_application.models import *
from home_application.esb_helper import get_business,get_host_by_app_id,get_host_config
from common.log import logger
import time
import datetime



# 获取用户下有权限的业务列表
def get_busines_by_user(request):
    try:
        ret = get_business(request.user.username)
        return render_json({'result':True,'data':ret})
    except Exception,e:
        logger.error(str(e))
        return render_json({'result':False})

# 获取主机数据库表的内容
def get_host(request):
    try:
        fitet_ip = request.GET.get('InnerIP','')
        ret = list(Server.objects.filter(ip__icontains=fitet_ip).values())
        return render_json({'result': True,'data':ret})
    except Exception,e:
        logger.error(str(e))
        return render_json({'result':False})

def get_host_by_id(request):
    try:
        get_id = request.GET.get('id','')
        ret = list(Server.objects.filter(id=get_id).values())
        return render_json({'result': True,'data':ret[0]})
    except Exception,e:
        logger.error(str(e))
        return render_json({'result':False})

def add_business(request):
    try:
        get_data = request.POST.dict()
        ret = get_host_by_app_id(request.user.username,get_data['app_info'])
        for i in ret:
            Server.objects.create(**i)

        res = get_host_config(ret)
        if res['result']:
            for i in res['data']:
                Server.objects.filter(ip=i['ip']).update(config_dsc=i['logContent'])
        return render_json({'result': True})
    except Exception,e:
        logger.error(str(e))
        return render_json({'result':False})

def del_server(request):
    try:
        get_data = request.POST.dict()
        Server.objects.filter(id=get_data['id']).delete()
        return render_json({'result': True})
    except Exception,e:
        logger.error(str(e))
        return render_json({'result':False})

