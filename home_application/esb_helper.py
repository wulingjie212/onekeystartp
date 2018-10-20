# -*- coding: utf-8 -*-


import requests
from conf.default import APP_ID, APP_TOKEN, BK_PAAS_HOST
import json
import base64
import time


def get_business(username):
    api_url = BK_PAAS_HOST + "/api/c/compapi/v2/cc/search_business/"
    get_data = {
        "bk_app_code": APP_ID,
        "bk_app_secret": APP_TOKEN,
        "bk_username": username,
    }
    res = requests.post(url=api_url, json=get_data)
    result = json.loads(res.content)
    if result['result']:
        ret = [{'app_id': i['bk_biz_id'], 'bussiness': i['bk_biz_name']} for i in result['data']['info'] if
               username in i['bk_biz_maintainer']]
    else:
        ret = []
    return ret


def get_host_by_app_id(username, app_id):
    api_url = BK_PAAS_HOST + "/api/c/compapi/v2/cc/search_host/"
    get_data = {
        "bk_app_code": APP_ID,
        "bk_app_secret": APP_TOKEN,
        "bk_username": username,
        "condition": [
            {"bk_obj_id": "biz",
             "fields": [],
             "condition": [
                 {"field": "bk_biz_id", "operator": "$eq", "value": int(app_id)}
             ]
             }
        ]
    }
    res = requests.post(url=api_url, json=get_data)
    result = json.loads(res.content)
    if result['result']:
        ret = [{'creator': username, 'app_id': i['biz'][0]['bk_biz_id'], 'bussiness': i['biz'][0]['bk_biz_name'],
                'source': i['host']['bk_cloud_id'][0]['bk_inst_id'], 'ip': i['host']['bk_host_innerip']} for i in
               result['data']['info']]
    else:
        ret = []
    return ret


def get_host_config(data):
    script_data = '''
    #!/bin/bash
DATE=$(date -R)
OS_VERSION=$(cat /etc/redhat-release)
OS_STRUCTURE=$(uname -m)
KERNEL_VERSION=$(uname -r)
CPU=$(grep 'model name' /proc/cpuinfo |uniq |awk -F : '{print $2}' |sed 's/^[ \t]*//g' |sed 's/ \+/ /g')
CPU_COUNTS=$(grep 'physical id' /proc/cpuinfo |sort |uniq |wc -l)
CPU_CORES=$(grep 'cpu cores' /proc/cpuinfo |uniq |awk -F : '{print $2}' |sed 's/^[ \t]*//g')
CPU_PROCESSOR=$(grep 'processor' /proc/cpuinfo |sort |uniq |wc -l)
CPU_MODE=$(getconf LONG_BIT)
TOTAL_MEM=$(cat /proc/meminfo |grep 'MemTotal' |awk -F : '{print $2}' |sed 's/^[ \t]*//g')
AVAILABLE_MEM=$(free -m |grep - |awk -F : '{print $2}' |awk '{print $2}')
TOTAL_SWAP=$(cat /proc/meminfo |grep 'SwapTotal' |awk -F : '{print $2}' |sed 's/^[ \t]*//g')
BUFFERS=$(cat /proc/meminfo |grep 'Buffers' |awk -F : '{print $2}' |sed 's/^[ \t]*//g')
CACHED=$(cat /proc/meminfo |grep '\<Cached\>' |awk -F : '{print $2}' |sed 's/^[ \t]*//g')
DISK=$(fdisk -l |grep 'Disk' |awk -F , '{print $1}' | sed 's/Disk identifier.*//g' | sed '/^$/d')
PARTITIONS=$(df -h |sed -n '2,$p')
# echo
echo -e "\n"
echo -e "TIME:${DATE}"
echo -e "\n"
echo -e "=== OS Class ==="
echo -e "OS_VERSION:\t${OS_VERSION}"
echo -e "OS_STRUCTURE:\t${OS_STRUCTURE}"
echo -e "KERNEL_VERSION:\t${KERNEL_VERSION}"
echo -e "\n"

echo -e "=== CPU Class ==="
echo -e "CPU:\t${CPU}"
echo -e "CPU_COUNTS:\t${CPU_COUNTS}"
echo -e "CPU_CORES:\t${CPU_CORES}"
echo -e "CPU_PROCESSOR:\t${CPU_PROCESSOR}"
echo -e "CPU_MODE:\t${CPU_MODE}"
echo -e "\n"

echo -e "=== Memory Class ==="
echo -e "TOTAL_MEMORY:\t${TOTAL_MEM}"
echo -e "AVALIABLE_MEMORY:\t${AVALIABLE_MEM}"
echo -e "TOTAL_SWAP:\t${TOTAL_SWAP}"
echo -e "BUFFERS:\t${BUFFERS}"
echo -e "CACHED:\t${CACHED}"
echo -e "\n"

echo -e "=== Disk Class ==="
echo -e "DISK:\t${DISK}"
echo -e "PARTITIONS:\n${PARTITIONS}"

    '''
    ret = fast_script(data[0]['creator'],data[0]['app_id'],[{'source':i['source'],'ip':i['ip']} for i in data],script_data)
    return ret

def fast_script(username, app_id, ip_list, script_content, account='root', script_type=1):
    # 快速执行脚本
    api_url = BK_PAAS_HOST + "/api/c/compapi/job/fast_execute_script/"
    api_head = {"Accept": "application/json"}
    get_data = {
        "app_code": APP_ID,
        "app_secret": APP_TOKEN,
        "username": username,
        "app_id": app_id,
        "content": base64.b64encode(script_content),
        'type': script_type,
        'ip_list': ip_list,
        'account': account
    }
    res = requests.post(url=api_url, json=get_data, headers=api_head)
    result = json.loads(res.content)
    if result["result"]:
        task_id = result["data"]["taskInstanceId"]
        time.sleep(2)
        return get_ip_log_content(task_id, username)
    else:
        return {"result": False, "data": result["message"]}


def get_ip_log_content(taskInstanceId, username, i=1):
    # 通过任务id，获取脚本作业的日志
    api_url = BK_PAAS_HOST + "/api/c/compapi/job/get_task_ip_log/"
    api_head = {"Accept": "application/json"}
    get_data = {
        "app_code": APP_ID,
        "app_secret": APP_TOKEN,
        "username": username,
        "task_instance_id": taskInstanceId,
    }
    res = requests.post(url=api_url, json=get_data, headers=api_head)
    result = json.loads(res.content)
    if result["result"]:
        if result["data"][0]["isFinished"]:
            ip_log_content = []
            for i in result["data"][0]["stepAnalyseResult"]:
                if i["resultType"] == 9:
                    ip_log_content.extend([{"result": True, "ip": str(j["ip"]), "logContent": j["logContent"]} for j in
                                           i["ipLogContent"]])
                else:
                    ip_log_content.extend([{"result": False, "ip": str(j["ip"]), "logContent": j["logContent"]} for j in
                                           i["ipLogContent"]])
            return {"result": True, "data": ip_log_content}
        else:
            time.sleep(1)
            return get_ip_log_content(taskInstanceId, username)
    else:
        i += 1
        if i < 12:
            time.sleep(5)
            return get_ip_log_content(taskInstanceId, username, i)
        else:
            err_msg = "get_logContent_timeout;task_id:%s;err_msg:%s" % (taskInstanceId, result["message"])
            return {"result": False, "data": err_msg}
