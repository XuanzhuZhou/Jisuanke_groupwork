# -*- coding: utf-8 -*-
'''
这个模块是接受 POST 请求。
可以用来给前端提供后台接口。
处理客户操作页面的api。
'''

import datetime
import json

from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.http import require_http_methods

from api.models import VerifyCode
from courses.models import Courses, Section
from datas.models import RefundRecord
from statuscode import REFUND_STATUS, STATUS_CODE, USER_TYPE
from users.models import User

from .models import Customer, get_info


def get_courses(username) -> list:
    """
    本函数用于获得用户课程信息

    :传入数据：username

    :返回数据: list[dist] 用户的课程信息

    """
    course_list = [{'username': username}]
    customers = User.objects.get(username=username).customer.all()
    if not customers.exists():
        return course_list
    for customer in customers:
        courses = customer.takes.all()
        for j in range(courses.count()):
            child_name = customer.child_name
            teacher = courses[j].teacher_id.name
            temp_dict = courses.values()[j]
            temp_dict['child_name'] = child_name
            temp_dict['teacher_name'] = teacher
            apply = RefundRecord.objects.filter(
                customer=customer,
                course=courses[j])
            if apply.count() > 0:
                temp_dict['refund_apply'] = (
                    REFUND_STATUS['Under Review'])
                if apply[0].is_passed:
                    temp_dict['refund_apply'] = (
                        REFUND_STATUS['Audit Passed'])
                    if apply[0].is_paid:
                        temp_dict['refund_apply'] = (
                            REFUND_STATUS['Already Paid'])
            else:
                temp_dict['refund_apply'] = (
                    REFUND_STATUS['No Refund Received'])
            course_list.append(temp_dict)
    return course_list


def get_sections(course_id) -> list:
    """
    本函数用于获得课程的课节信息

    :传入数据：course_id 课程id

    :返回数据: list  课节信息

    """
    try:
        course = Courses.objects.get(id=course_id)
    except Courses.DoesNotExist:
        return []
    sections = Section.objects.filter(
        course_id=course).order_by('-date').values()
    return list(sections)


def refund_apply(data, username):
    """
    本函数用于处理家长退款信息的内部处理

    :传入数据：data {'info', 'course_id', 'child_name'} , username

    :返回数据: 状态码 0 或 903

    """
    info = data['info']
    course_id = data['course_id']
    child_name = data['child_name']
    customer = Customer.objects.get(
        user=User.objects.get(username=username), child_name=child_name)
    try:
        course = Courses.objects.get(id=course_id)
    except Courses.DoesNotExist:
        return STATUS_CODE['Course Not Found']
    cc = customer.cc
    RefundRecord.objects.create(
        customer=customer,
        course=course,
        cc=cc,
        reason=info).save()
    return STATUS_CODE['Success']


def try_register(data):
    """
    本函数用于在内部验证注册请求

    :传入数据：data {'code' 'username' 'child_name'}

    :返回数据: 状态码 0 或 707 或 905

    """
    if 'code' not in data or 'username' not in data:
        return STATUS_CODE['Verify Code Error']
    code = data['code']
    tel = data['username']
    verify = VerifyCode.objects.filter(
        code=code, tel=tel).order_by('-add_time')
    if verify.count() == 0:
        return STATUS_CODE['Verify Code Error']
    delta = (timezone.now() - verify[0].add_time).total_seconds()
    VerifyCode.objects.filter(tel=tel).delete()
    if delta <= 0 or delta > 120:
        return STATUS_CODE['Verify Code Error']
    user = User.objects.get_or_create(username=data['username'])
    if user[1]:
        user[0].is_active = False
    user[0].save()
    cus = Customer.objects.get_or_create(
        user=user[0], child_name=data['child_name'])
    if cus[1] or not cus[0].is_paid:
        cus[0].save()
        return STATUS_CODE['Success']
    return STATUS_CODE['Customer Already Exists']


@login_required
@require_http_methods(['POST'])
def view_courses(request):
    """
    本api用于处理客户查看课程信息请求

    :前端传入数据: 无 要求家长登录

    :url: customer/courses

    :返回数据: key: 'list': 课程信息 key: 'msg' 状态码 0 或 901

    :返回样例：[{'username': 'customer'},

            {'id': 1, 'name': 'course1', 'teacher_id_id': 1,

            'time': None, 'date': 0, 'total_sec': 30,

            'price': None, 'child_name': 'child1',

            'teacher_name': 'teacher1', 'refund_apply': 0}]

    :数据内容: [用户名 课程id 课名 老师id 时间 星期 课节总数 价格

                孩子姓名 老师姓名 退款状态]
    """
    user = request.user
    response = {}
    if user.user_type == USER_TYPE['customer']:
        response['msg'] = STATUS_CODE['Success']
        response['list'] = get_courses(user.username)
    else:
        response['msg'] = STATUS_CODE['Identity Error']
    return JsonResponse(response)


@login_required
@require_http_methods(['POST'])
def customer_info(request):
    """
    本api用来处理家长查看孩子信息的请求

    :传入数据：无 要求登录

    :url: customer/info

    :返回数据: key: 'list': 孩子信息; key: 'msg' 状态码 0 或 901

    :返回样例： [{'id': 5, 'user_id': 7, 'child_name': 'child1',

                'parent_name': None, 'classin_id': None,

                'classin_name': None, 'birthday': None,

                'cc_id': 'consultant', 'audition_count': 0,

                'is_signedup': False, 'is_paid': True,

                'old_user_id': None, 'date_cc': None,

                'demand': None, 'gender': None}
    """
    user = request.user
    response = {}
    if user.user_type == USER_TYPE['customer']:
        response['msg'] = STATUS_CODE['Success']
        response['list'] = get_info(user.username)
    else:
        response['msg'] = STATUS_CODE['Identity Error']
    return JsonResponse(response)


@login_required
@require_http_methods(['POST'])
def refund(request):
    """
    本api用来处理家长退款的请求

    :url: customer/refund

    :前端传入数据：'info', 'course_id', 'child_name'

    :返回数据: 状态码 0 或 903 或 901

    """
    user = request.user
    data = json.loads(request.body)
    response = {}
    if user.user_type == USER_TYPE['customer']:
        response['msg'] = refund_apply(data, user.username)
    else:
        response['msg'] = STATUS_CODE['Identity Error']
    return JsonResponse(response)


@login_required
@require_http_methods(['POST'])
def refund_cancel(request):
    """
    本api用来处理家长取消退款的请求

    :url: customer/refund_cancel

    :前端传入数据: 'course_id', 'child_name'

    :返回数据: 状态码 0 或 901

    """
    user = request.user
    data = json.loads(request.body)
    response = {}
    if user.user_type == USER_TYPE['customer']:
        course = Courses.objects.get(id=data['course_id'])
        customer = Customer.objects.get(
            user=request.user,
            child_name=data['child_name']
        )
        for refund_record in course.refund_record.filter(customer=customer):
            refund_record.delete()
        response['msg'] = STATUS_CODE['Success']
    else:
        response['msg'] = STATUS_CODE['Identity Error']
    return JsonResponse(response)


@require_http_methods(['POST'])
def register(request):
    """
    本api用来处理家长注册的请求

    :url: customer/register

    :前端传入数据: username child_name code

    :返回数据: 状态码 0 或 707 或 905

    """
    data = json.loads(request.body)
    response = {}
    response['msg'] = try_register(data)
    return JsonResponse(response)


@require_http_methods(['POST'])
def register_success(request):
    """
    本api用来处理家长注册成功后激活的请求

    :url: customer/register_success

    :前端传入数据: username child_name

    :返回数据: 状态码 0 或 902 或 705

    """
    data = json.loads(request.body)
    response = {}
    if 'username' in data and 'child_name' in data:
        try:
            user = User.objects.get(username=data['username'])
            user.set_password(user.username[5:])
            user.user_type = USER_TYPE['customer']
            user.is_active = True
            customer = Customer.objects.get(
                user=user, child_name=data['child_name'])
            customer.is_paid = True
            user.save()
            customer.save()
            response['msg'] = STATUS_CODE['Success']
        except (User.DoesNotExist, Customer.DoesNotExist):
            response['msg'] = STATUS_CODE['User Not Found']
    else:
        response['msg'] = STATUS_CODE['Frontend Value Error']
    return JsonResponse(response)


@login_required
@require_http_methods(['POST'])
def view_sections(request):
    """

    本api用来处理家长查看课程相应课节的请求

    :url: customer/sections

    :前端传入数据: course_id

    :返回数据：key: 'msg' 状态码 0或901 key: 'list' 课节信息

    :返回样例： [{'id': 1, 'course_id_id': 41, 'count': 1, 'name': None,

                'date': datetime.date(2000, 2, 2),

                'start_time': datetime.time(0, 0, 1),

                'end_time': datetime.time(0, 0, 2),

                'location': 'location', 'is_cancel': False}...]

    :数据内容: [课节id 课程id 课节序 课节名 上课日期  开始时间

                结束日期 地点 是否销课]

    """

    data = json.loads(request.body)
    response = {}
    if request.user.user_type == USER_TYPE['customer']:
        response['list'] = get_sections(data['course_id'])
        response['msg'] = STATUS_CODE['Success']
    else:
        response['msg'] = STATUS_CODE['Identity Error']
    return JsonResponse(response)


@require_http_methods(['POST'])
def customer_login_password(request):
    """
    本api用来处理家长用密码登录的请求

    :url: customer/login_password

    :前端传入数据: username password

    :返回数据: 状态码 0 或 901 或 705 或 709 或 902

    """
    response = {}
    data = json.loads(request.body)
    if 'password' not in data or 'username' not in data:
        response['msg'] = STATUS_CODE['Frontend Value Error']
        return JsonResponse(response)
    username = data['username']
    user = User.objects.filter(username=username)
    if user.count() == 0:
        response['msg'] = STATUS_CODE['User Not Found']
        return JsonResponse(response)
    if user[0].check_password(data['password']):
        if user[0].user_type == USER_TYPE['customer']:
            auth.login(request, user[0])
            response['msg'] = STATUS_CODE['Success']
        else:
            response['msg'] = STATUS_CODE['Identity Error']
    else:
        response['msg'] = STATUS_CODE['Password Not Match']
    return JsonResponse(response)


@require_http_methods(['POST'])
def customer_login_code(request):
    """
    本api用来处理家长用验证码登录的请求

    :url: customer/login_code

    :前端传入数据: username code

    :返回数据: 状态码 0 或 901 或 705 或 707 或 902

    """
    response = {}
    data = json.loads(request.body)
    if 'code' not in data or 'username' not in data:
        response['msg'] = STATUS_CODE['Frontend Value Error']
        return JsonResponse(response)
    username = data['username']
    user = User.objects.filter(username=username)
    if user.count() == 0 or user[0].is_active is False:
        response['msg'] = STATUS_CODE['User Not Found']
        return JsonResponse(response)
    verify = VerifyCode.objects.filter(
        code=data['code'], tel=username).order_by('-add_time')
    if verify.count() == 0:
        response['msg'] = STATUS_CODE['Verify Code Error']
        return JsonResponse(response)
    delta = (timezone.now() - verify[0].add_time).total_seconds()
    VerifyCode.objects.filter(tel=username).delete()
    if delta <= 0 or delta > 120:
        response['msg'] = STATUS_CODE['Verify Code Error']
        return JsonResponse(response)
    if user[0].user_type == USER_TYPE['customer']:
        auth.login(request, user[0])
        response['msg'] = STATUS_CODE['Success']
    else:
        response['msg'] = STATUS_CODE['Identity Error']
    return JsonResponse(response)


@login_required
@require_http_methods(['POST'])
def view_pay_records(request):
    """
    本api用来处理家长查看付款记录的请求

    :url: customer/pay_records

    :前端传入数据: 无 要求登录

    :返回数据: 'msg': 状态码 0 或 901 'list': 记录信息

    :数据样例: .[{'id': 21, 'money': 30.0,

                'date': '2018-08-25 17:15:58', 'info': 'test',

                'is_paid': False, 'child_name': 'child1',

                'cc_name': 'consultant'}..]

    :数据内容: [记录id 金额 时间 详细信息 是否结款 孩子姓名 cc名字]

    """
    response = {}
    response['list'] = []
    if request.user.user_type == USER_TYPE['customer']:
        for customer in request.user.customer.all():
            if customer.cc:
                cc_name = customer.cc.username
            else:
                cc_name = 'null'
            records = customer.signup_record.all()
            records = list(
                records.values('id', 'money', 'date', 'info', 'is_paid'))
            for record in records:
                record['child_name'] = customer.child_name
                record['cc_name'] = cc_name
                record['date'] = (
                    datetime.datetime.strftime(
                        record['date'], '%Y-%m-%d %H:%M:%S'))
                response['list'].append(record)
        response['msg'] = STATUS_CODE['Success']
    else:
        response['msg'] = STATUS_CODE['Identity Error']
    return JsonResponse(response)
