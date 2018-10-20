import requests
from conf.default import *
import base64
# urls = 'http://paas.canway.club/api/c/compapi/v2/job/fast_execute_script/'
# data = {'bk_app_code':APP_ID,'bk_app_secret':APP_TOKEN,
#             'bk_username':'admin',
#     "bk_biz_id": 2,
#     "script_content": base64.b64encode('hostname'),
#     "account": "root",
#     "script_type": 1,
#     "ip_list": [
#         {
#             "bk_cloud_id": 0,
#             "ip": "192.168.169.13"
#         },
#         {
#             "bk_cloud_id": 0,
#             "ip": "192.168.169.12"
#         }
#     ],
#     }
# ret = requests.post(url=urls,json=data)
# print ret.content


urls = 'http://paas.canway.club/api/c/compapi/v2/job/get_job_instance_log/'
data = {'bk_app_code':APP_ID,'bk_app_secret':APP_TOKEN,
            'bk_username':'admin',
    "bk_biz_id": 2,
    "job_instance_id":8935
    }
ret = requests.post(url=urls,json=data)
print ret.content