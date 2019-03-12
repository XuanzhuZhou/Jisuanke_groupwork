# -*- coding: utf-8 -*-

'''
这个模块是接受 GET 和 POST 请求的样例。
可以用来给前端提供后台测试接口。
'''
# from django.shortcuts import render

import json
import os
from datetime import datetime, timedelta

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

import qrcode
from customers.models import Customer
from datas.models import OperationLogs
from PIL import Image
from server.settings import HOME_UPR, MEDIAFILES_DIRS
from statuscode import STATUS_CODE, USER_TYPE

from .models import SellerInfo, User

# Create your views here.


def generate_qrcode(info, home, path):
    """
    本函数用于生成二维码

    :接受数据：info(seller info 赋给index) home(根网址) path(保存路径)

    :返回值: 无

    """
    if not os.path.exists(path):
        os.makedirs(path)
    theqr = qrcode.QRCode(
        version=10,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=3, border=2)
    name = ''.join([str(info), '.png'])
    theqr.add_data(os.path.join(home, ''.join(['?index=', str(info)])))
    theqr.make()
    img = theqr.make_image()
    img = img.convert("RGBA")
    img_width, img_height = img.size
    width, height = map(lambda x: x//4, img.size)
    im_pate = os.path.join(
        MEDIAFILES_DIRS[0] + '/img', 'headpic.png')
    if os.path.exists(im_pate):
        im_in = Image.open(im_pate)
        im_width, im_height = im_in.size
        width = width if width < im_width else im_width
        height = height if height < im_height else im_height
        im_in = im_in.resize((width, height))
        img.paste(im_in, ((img_width-width)//2, (img_height-height)//2))
    path = os.path.join(path, name)
    with open(path, 'wb') as image_file:
        img.save(image_file, 'PNG')


@login_required
@require_http_methods(['POST'])
def get_qrcode(request):
    """
    本函数用于处理获得二维码请求返回二维码路径

    :前端发送数据: 登录后的请求数据

    :url: user/qrcode

    :返回: Success 或 Identity Error 状态码

    :返回值: Json字典

    :返回样例1(成功): {'msg': 0}

    :返回样例2(身份错误): {'msg': 901}

    """
    response = {}
    username = request.user.username
    user = User.objects.get(username=username)
    if not user.user_type == USER_TYPE['seller']:
        response['msg'] = STATUS_CODE['Identity Error']
        return JsonResponse(response)
    seller_id = SellerInfo.objects.get(seller=user).id
    name = ''.join([str(seller_id), '.png'])
    path = os.path.join('/static/img/', name)
    path_real = os.path.join(
        MEDIAFILES_DIRS[0] + '/img', name)
    if not os.path.exists(path_real):
        generate_qrcode(seller_id, HOME_UPR, os.path.dirname(path_real))
    response['msg'] = STATUS_CODE['Success']
    response['path'] = path
    return JsonResponse(response)


def create_timedelta(start, end):
    '''本函数用来返回时间差'''
    result = {}
    if start is None and end is None:
        end = datetime.now() + timedelta(hours=24)
        start = end - timedelta(hours=30*24)
    elif start is None:
        end = datetime.strptime(end, "%Y-%m-%d")
        start = end - timedelta(hours=30*24)
    elif end is None:
        start = datetime.strptime(start, "%Y-%m-%d")
        end = start + timedelta(hours=30*24)
    start = start.strftime("%Y-%m-%d")
    end = end.strftime("%Y-%m-%d")
    result['start'] = start
    result['end'] = end
    return result


@login_required
@require_http_methods(['POST'])
def superuser_viewlog(request):
    """
    本函数用来响应前端请求查看日志

    :url: user/superuser_viewlog

    :前端发送数据: {'start': '起始日期', 'end': '结束日期'}

    :返回: error标识和日志信息

    :返回值: Json字典

    :返回样例1(成功): {'error': 0, 'list': [{'id': 1, 'type': 1,

                'username': 'person1', 'date': '2018-08-21',

                'info': 'superuser删除了员工person1',

                'operator': 'superuser'}]}

    :返回样例2(无结果): {'error': 1}
    """
    response = {}
    data = json.loads(request.body)
    start = data['start']
    end = data['end']
    if start is None or end is None:
        result = create_timedelta(start, end)
        start = result['start']
        end = result['end']
    logs = OperationLogs.objects.filter(
        date__range=[start, end])
    if logs.count() == 0:
        response['error'] = STATUS_CODE['Not Found']
        return JsonResponse(response)
    response['error'] = STATUS_CODE['Success']
    logs = list(logs.values())
    res_list = []
    for log in logs:
        temp_dict = log
        operator = User.objects.get(pk=temp_dict.pop('operator_id')).username
        temp_dict['operator'] = operator
        temp_dict['date'] = temp_dict['date'].strftime('%Y-%m-%d')
        res_list.append(temp_dict)
    response['list'] = res_list
    return JsonResponse(response)


@login_required
@require_http_methods(['POST'])
def superuser_view_newstu(request):
    """
    本函数用于前端发送请求获取待分配课程顾问的学生及家长信息

    :url: user/superuser_view_newstu

    :返回: error标识和学生及家长信息

    :返回值: Json字典

    :返回样例1(成功): {'error': 0, 'list': [{'id': 1, 'child_name': 'child1',

                'parent_name': None, 'demand': None,

                'tel': '13812349874'}]}

    :返回样例2(无结果): {'error': 1}
    """
    response = {}
    customers = Customer.objects.filter(cc=None)
    if customers.count() == 0:
        response['error'] = STATUS_CODE['Not Found']
        return JsonResponse(response)
    response['error'] = STATUS_CODE['Success']
    res_list = []
    customers = list(customers.values())
    for customer in customers:
        temp_dict = customer
        user_id = temp_dict.pop('user_id')
        temp_dict['tel'] = User.objects.get(pk=user_id).username
        del temp_dict['classin_id']
        del temp_dict['classin_name']
        del temp_dict['is_paid']
        del temp_dict['cc_id']
        del temp_dict['is_signedup']
        del temp_dict['birthday']
        del temp_dict['old_user_id']
        del temp_dict['audition_count']
        del temp_dict['date_cc']
        res_list.append(temp_dict)
    response['list'] = res_list
    return JsonResponse(response)


@login_required
@require_http_methods(['POST'])
def superuser_get_cc(request):
    """
    本函数用于前端发送请求获取课程顾问信息和资源数

    :url: user/superuser_get_cc

    :返回: error标识和课程顾问信息

    :返回值: Json字典

    :返回样例1(成功): {'error': 0, 'list': [{'id': 2, 'username': 'cc0', 'gender':

                'female', 'count': 1},{'id': 3, 'username': 'cc1', 'gender':

                'female', 'count': 0},{'id': 4, 'username': 'cc2', 'gender':

                'female', 'count': 0}]}

    :返回样例2(无结果): {'error': 1}
    """

    response = {}
    consults = User.objects.filter(user_type=USER_TYPE['consultant'])
    if consults.count() == 0:
        response['error'] = STATUS_CODE['Not Found']
        return JsonResponse(response)
    consults = list(consults.values())
    res_list = []
    for consult in consults:
        temp_dict = {}
        temp_dict['id'] = consult['id']
        temp_dict['username'] = consult['username']
        temp_dict['gender'] = consult['gender']
        cc = User.objects.get(pk=temp_dict['id'])
        count = cc.cc_customers.count()
        temp_dict['count'] = count
        res_list.append(temp_dict)
    response['error'] = STATUS_CODE['Success']
    response['list'] = res_list
    return JsonResponse(response)


@login_required
@require_http_methods(['POST'])
def superuser_arrange_cc(request):
    """
    本函数用于前端发送请求和数据分配课程顾问

    :前端发送数据: {'customer_id': '家长的id', 'cc_id': 'cc的id'}

    :url: user/superuser_arrange_cc

    :返回: error标识

    :返回值: Json字典

    :返回样例1(成功): {'error': 0}

    :返回样例2(用户未找到): {'error': 1}
    """
    response = {}
    data = json.loads(request.body)
    customer_id = data['customer_id']
    cc_id = data['cc_id']
    try:
        customer = Customer.objects.get(pk=customer_id)
    except Customer.DoesNotExist:
        response['error'] = STATUS_CODE['Not Found']
        return JsonResponse(response)
    try:
        cc = User.objects.get(pk=cc_id)
    except User.DoesNotExist:
        response['error'] = STATUS_CODE['Not Found']
        return JsonResponse(response)
    customer.cc = cc
    customer.save()
    response['error'] = STATUS_CODE['Success']
    return JsonResponse(response)
