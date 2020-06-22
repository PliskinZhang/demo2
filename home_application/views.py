# -*- coding: utf-8 -*-
from django.shortcuts import render


# 开发框架中通过中间件默认是需要登录态的，如有不需要登录的，可添加装饰器login_exempt
# 装饰器引入 from blueapps.account.decorators import login_exempt

from blueking.component.shortcuts import get_client_by_user,get_client_by_request
from django.http import JsonResponse,HttpResponse
import json
import base64

def home(request):
    """
    首页
    """
    return render(request, 'home_application/home.html')


def contact(request):
    """
    联系我们
    """
    return render(request, 'home_application/contact.html')

def list_business(request):
    client = get_client_by_request(request)
    reqData={
        "fields": [
            "bk_biz_id",
            "bk_biz_name"
        ]
    }
    rspData = client.cc.search_business(reqData)
    if rspData['result'] == True:
        data = rspData['data']
        return HttpResponse(json.dumps(data['info']))

def doFastJob(request):
    bk_biz_id = request.GET.get('bk_biz_id')
    client = get_client_by_request(request)
    username = request.user.username
    script = 'df -h'
    reqData = {'bk_biz_id': bk_biz_id,
               # 'script_id': script_id,
               # 'script_param': str(base64.b64encode(param.encode("utf8")), "utf8"),
               "script_content": str(base64.b64encode(script.encode("utf8")), "utf8"),
               'account': 'root',
               'script_type': 1,
               'ip_list': [
                {
                 "bk_cloud_id": 0,
                 "ip": "192.168.1.21"
                }]
               }
    rspData = client.job.fast_execute_script(reqData)
    if rspData['result'] == True:
        jobInstaceId = rspData['data']['job_instance_id']


# def jobResult(request):



