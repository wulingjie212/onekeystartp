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

from django.db import models

class Server(models.Model):
    app_id = models.IntegerField()
    bussiness = models.CharField(max_length=50)
    ip = models.CharField(max_length=20)
    source = models.IntegerField()
    creator = models.CharField(max_length=10)
    config_dsc = models.TextField()
    cpu_monitor = models.TextField()

class demo(models.Model):
    name = models.TextField()
    value = models.CharField(max_length=50)