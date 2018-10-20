# -*- coding: utf-8 -*-
"""
Tencent is pleased to support the open source community by making 蓝鲸智云(BlueKing) available.
Copyright (C) 2017 THL A29 Limited, a Tencent company. All rights reserved.
Licensed under the MIT License (the "License"); you may not use this file except in compliance with the License.
You may obtain a copy of the License at http://opensource.org/licenses/MIT
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and limitations under the License.
"""

from common.mymako import render_mako_context,render_json
from django.db.models import Q
import requests

def home(request):
    """
    首页
    """
    return render_mako_context(request, '/onekey_home/index.html')


def dev_guide(request):
    """
    开发指引
    """
    return render_mako_context(request, '/home_application/dev_guide.html')

def onekey_conf(request):
    return render_mako_context(request, '/onekey_home/detail.html')

def detail(request):
    """
    开发指引
    """
    return render_mako_context(request, '/onekey_home/detail.html')


def tab(request):
    """
    联系我们
    """
    return render_mako_context(request, '/onekey_home/tab.html')

def contactus(request):
    """
    联系我们
    """
    # 修改数据
    # 创建虚拟机
    # return render_json({'data':'hello world'})
    return render_mako_context(request, '/home_application/contact.html')

from home_application.models import demo
# from home_application.celery_tasks import async_task
import datetime
def test(request):
    # date = datetime.datetime.now() + datetime.timedelta(seconds=20)
    # print datetime.datetime.now()
    # async_task.apply_async(args=['1'], eta=date)

    return render_mako_context(request, '/home_application/test.html')

def demos(request):
    return render_mako_context(request, '/home_application/demo.html')


from conf.default import *
from esb_helper import fast_script
def get_demo_data(request):
    ret = list(demo.objects.all().values())
    return render_json({'data':ret})