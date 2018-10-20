# -*- coding: utf-8 -*-
"""
Tencent is pleased to support the open source community by making 蓝鲸智云(BlueKing) available.
Copyright (C) 2017 THL A29 Limited, a Tencent company. All rights reserved.
Licensed under the MIT License (the "License"); you may not use this file except in compliance with the License.
You may obtain a copy of the License at http://opensource.org/licenses/MIT
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and limitations under the License.

celery 任务示例

本地启动celery命令: python  manage.py  celery  worker  --settings=settings
周期性任务还需要启动celery调度命令：python  manage.py  celerybeat --settings=settings
"""
import datetime

from celery import task
from celery.schedules import crontab
from celery.task import periodic_task
from home_application.models import *
from home_application.esb_helper import fast_script

from common.log import logger


# @periodic_task(run_every=crontab(minute='*/1', hour='*', day_of_week="*"))
# def async_task():
#     print datetime.datetime.now()
#     print '111111111'

#
# def execute_task():
#     """
#     执行 celery 异步任务
#
#     调用celery任务方法:
#         task.delay(arg1, arg2, kwarg1='x', kwarg2='y')
#         task.apply_async(args=[arg1, arg2], kwargs={'kwarg1': 'x', 'kwarg2': 'y'})
#         delay(): 简便方法，类似调用普通函数
#         apply_async(): 设置celery的额外执行选项时必须使用该方法，如定时（eta）等
#                       详见 ：http://celery.readthedocs.org/en/latest/userguide/calling.html
#     """
#     now = datetime.datetime.now()
#     logger.error(u"celery 定时任务启动，将在60s后执行，当前时间：{}".format(now))
#     # 调用定时任务
#     async_task.apply_async(args=[now.hour, now.minute], eta=now + datetime.timedelta(seconds=60))


@periodic_task(run_every=crontab(minute='*/1', hour='*', day_of_week="*"))
def get_cpu():
    all_data = {}
    script_data = 'sar -u 1 1'
    for i in Server.objects.all():
        if all_data.get(i.app_id,False):
            all_data[i.app_id].append({'ip':i.ip,'source':i.source})
        else:
            all_data[i.app_id] = [{'ip':i.ip,'source':i.source}]
    for z in all_data.keys():
        ret = fast_script('admin', z, all_data[z],script_data)
        if ret['result']:
            for x in ret['data']:
                for cell_line in x['logContent'].split('\n'):
                    if 'Average:' in cell_line:
                        Server.objects.filter(ip=x['ip'],app_id=z).update(cpu_monitor=cell_line.split()[3])