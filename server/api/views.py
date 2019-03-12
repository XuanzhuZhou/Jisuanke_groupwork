# -*- coding:  utf-8 -*-

'''本文件用于实现 api 接口'''


import json
import os
import random
import time
from datetime import date, datetime, timedelta

from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.serializers import serialize
from django.db import DatabaseError, transaction
from django.db.models import Q
from django.http import HttpResponse, JsonResponse, QueryDict
from django.views.decorators.http import require_http_methods

from courses.models import Courses, Section, Teacher
from courses.views import get_teacher_info
from customers.models import (Customer, get_info, modify_customer_info)
from datas.models import (CcRecord, OperationLogs, RefundRecord, SellRecord,
                          import_customer_info)
from datas.views import get_records_money
from statuscode import (LOG_TYPE, REFUND_STATUS, STATUS_CODE,
                        TRADE_TYPE, USER_TYPE)
from users.models import (SellerInfo, User, get_or_create_default_seller,
                          modify_user_info, search_user_info)
from users.views import create_timedelta

from .alibaba import check_notify, product_trade_no, solve_trade
from .models import VerifyCode, check_mobile, send_message

DEBUG = True


@require_http_methods(['POST'])
def check_login(request):
    """
    本api用于实现登录检查和页面跳转检查

    :url: api/check_login

    :返回: error状态码

    :返回值: Json字典

    :返回样例: {'error': 0}或{'error': 1}

    :状态码解释: 0 已登录且身份符合 1未登录或者身份不匹配
    """
    response = {}
    if request.user.is_authenticated:
        response['user_type'] = request.user.user_type
        response['error'] = STATUS_CODE['Success']
        return JsonResponse(response)
    response['error'] = STATUS_CODE['Not Found']
    return JsonResponse(response)


@require_http_methods(['POST'])
def login(request):
    """
    本api用于实现后台员工登录

    :url: api/login

    :前端传入数据(样例):  data = {'type': '3', 'user': 'username',

    'password': 'password'}

    :返回: error状态码

    :返回值: Json字典

    :返回样例(成功): {'error': 0}

    :状态码解释: 0(允许登录) 902(未找到用户) 901(身份不匹配) 709(密码不正确)
    """
    response = {}
    data = json.loads(request.body)
    username = data['user']
    user = User.objects.filter(username=username)
    if user.count() == 0:
        response['error'] = STATUS_CODE['User Not Found']
        return JsonResponse(response)
    if user[0].check_password(data['password']):
        if user[0].user_type == int(data['type']):
            auth.login(request, user[0])
            response['error'] = STATUS_CODE['Success']
            return JsonResponse(response)
        response['error'] = STATUS_CODE['Identity Error']
        return JsonResponse(response)
    response['error'] = STATUS_CODE['Password Not Match']
    return JsonResponse(response)


@login_required
@require_http_methods(['POST'])
def logout(request):
    """
    本api用于退出登录

    :url: api/logout

    :返回: error状态码

    :返回值: Json字典

    :返回样例(成功): {'error': 0}
    """
    response = {}
    auth.logout(request)
    response['error'] = STATUS_CODE['Success']
    return JsonResponse(response)


@login_required
@require_http_methods(['POST'])
def change_password(request):
    """
    本api用于修改密码

    :url: api/change_password

    :前端传送数据: data = {'username': 'username', 'old_psw': 'old_psw',

    'new_psw': 'new_psw'}

    :返回: error状态码

    :返回值: Json字典

    :返回样例: {'error': 0}

    :状态码解释: 0(成功更改密码) 709(原密码错误)
    """
    response = {}
    data = json.loads(request.body)
    username = data['username']
    old_psw = data['old_psw']
    new_psw = data['new_psw']
    user = auth.authenticate(username=username, password=old_psw)
    if user is not None and user.is_active:
        user.set_password(new_psw)
        user.save()
        response['error'] = STATUS_CODE['Success']
    else:
        response['error'] = STATUS_CODE['Password Not Match']
    return JsonResponse(response)


@require_http_methods(['POST'])
def recieve_message_request(request):
    '''
    处理发送短信请求

    :url: api/sendmsg

    :前端传送数据: data = {'tel': '12345677654'}

    :返回: Json字典
    '''
    data = json.loads(request.body)
    tel = data['tel']
    code = send_message(tel)
    response = {}
    if not code:
        response['msg'] = STATUS_CODE['Error Tel Number']
        return JsonResponse(response)
    try:
        with transaction.atomic():
            member = VerifyCode.objects.filter(tel=tel)
            if member.count() > 0:
                member = member.order_by('-add_time')[0]
                member.code = code
                member.save()
                response['msg'] = STATUS_CODE['Success']
                return JsonResponse(response)
            member = VerifyCode(code=code, tel=tel)
            member.save()
    except DatabaseError as error:
        print("Error:\n\t", error)
        response['msg'] = STATUS_CODE['Database Error']
        return JsonResponse(response)
    response['msg'] = STATUS_CODE['Success']
    return JsonResponse(response)


def get_pay_type(agent) -> int:
    """
    根据请求来源判断支付类型

    :传入参数: 浏览器发出的用户 agent 信息

    :返回信息: 根据传入参数判断得出的支付类型(参考 TRADE_TYPE)
    """
    return TRADE_TYPE['wap_pay'] if check_mobile(
        agent) else TRADE_TYPE['page_pay']


def get_customer_and_seller(data: dict) -> tuple:
    """
    根据data中的 tel、child_name、seller_id 获取 cuatomer 和 seller

    :传入参数: 从前端 json 信息中提取出的字典类型，调用本函数前应检查参数是否齐全

    :返回信息: customer 和 seller，如果没找到则返回 (None, None)

    """
    user = User.objects.filter(username=data['tel'])
    if not user.exists():
        return None, None
    user = user.first()
    customer = Customer.objects.filter(
        user=user, child_name=data['child_name'])
    if not customer.first():
        return None, None
    customer = customer.first()
    if data['seller_id'] == '-1':
        seller = get_or_create_default_seller()
    else:
        seller = SellerInfo.objects.filter(id=data['seller_id'])
    if not seller:
        return customer, None
    return customer, seller


@require_http_methods(['POST'])
def deal_register_pay(request):
    """
    处理注册时的支付请求

    :传入参数: HttpRequest 请求

    :返回参数: 支付宝的支付地址

    """
    data = json.loads(request.body)
    if not check_front_key_exists(data, ('tel', 'child_name', 'seller_id')):
        return get_status_response('Frontend Value Error')
    customer, seller = get_customer_and_seller(data)
    if not customer or not seller:
        return get_status_response('User Not Found')
    price = seller.price
    trade_no = product_trade_no()
    pay_type = get_pay_type(request.META['HTTP_USER_AGENT'])
    url = solve_trade(pay_type, trade_no=trade_no, amount=price)
    try:
        with transaction.atomic():
            seller_record = SellRecord.objects.create(
                customer=customer, seller=seller,
                money=price, trade_no=trade_no)
            seller_record.save()
    except DatabaseError as error:
        print("DatabaseError when insert into SellRecord\n", error)
        return get_status_response('Database Error')
    response = {'url': url, 'msg': STATUS_CODE['Success']}
    return JsonResponse(response)


def get_alipay_notify(request) -> HttpResponse:
    """
    接收处理支付宝的回调信息

    :参数: HttpRequest

    :返回值: HttpResposne

    """
    data = json.loads(request.body)
    if check_front_key_exists(data, ('sign', 'sign_type', 'out_trade_no')):
        return HttpResponse('Fail')
    if not check_notify(data):
        return HttpResponse('Fail')
    trade_no = data['out_trade_no']
    if SellerInfo.objects.filter(trade_no=trade_no):
        return register_paid(trade_no)
    if CcRecord.objects.filter(trade_no=trade_no):
        return class_paid(request)
    return HttpResponse('Fail')


def register_paid(trade_no):
    """
    本函数用于处理注册之后支付宝的回调信息，如果用户已经支付，则修改用户的状态

    :参数: trade_no: 订单号

    :返回值: HttpResponse

    """
    sell_record = SellRecord.objects.filter(trade_no=trade_no)
    if not sell_record.exists():
        return HttpResponse('Fail')
    sell_record = sell_record.first()
    user = sell_record.customer.user
    user.is_active = True
    user.save()
    return HttpResponse('success')


def get_ccrecord(data: dict) -> QueryDict:
    """
    本函数用于从前端 json 数据中提取 id 和 price, 找到对应的 ccrecord 记录, 并进行验证

    :传入参数: data 字典类型, 调用本函数前应先检查字典中的键是否全部存在

    :返回数据: QueryDict CcRecord 的查询结果，未查到返回 None

    """
    cc_record = CcRecord.objects.filter(id=data['id'])
    if not cc_record.exists():
        return None
    cc_record = cc_record.first()
    return cc_record


def class_paid(trade_no):
    """
    处理正式课程报名之后支付宝的回调信息, 如果用户支付, 则修改 CcRecord 中的状态

    :参数: trade_no: 订单号

    :返回值: HttpResponse

    """
    cc_record = CcRecord.objects.filter(trade_no=trade_no).first()
    try:
        with transaction.atomic():
            cc_record.is_paid = True
            cc_record.save()
            customer = cc_record.customer
            customer.takes.add(cc_record.course)
            customer.save()
    except DatabaseError as error:
        print("Error:\n", error)
        return HttpResponse('Fail')
    return HttpResponse('success')


@require_http_methods(['POST'])
def class_pay(request):
    """
    本函数用于处理正式课的支付请求，返回支付的url

    :参数: request: HttpRequest

    :返回值: JsonResponse 如果程序顺利执行，返回中带有跳转至支付宝所需要的 url,
            否则会带有错误码(参考 statuscode STATUS_CODE)

    """
    data = json.loads(request.body)
    if not check_front_key_exists(data, ('id',)):
        return get_status_response('Frontend Value Error')
    cc_record = get_ccrecord(data)
    if not cc_record:
        return get_status_response('Trade Record Exception')
    pay_type = get_pay_type(request.META['HTTP_USER_AGENT'])
    trade_no = cc_record.trade_no
    price = cc_record.money
    url = solve_trade(pay_type, trade_no=trade_no, amount=price)
    if not url:
        return get_status_response('Alipay Error')
    if DEBUG:
        try:
            with transaction.atomic():
                cc_record.is_paid = True
                cc_record.save()
                customer = cc_record.customer
                customer.takes.add(cc_record.course)
                customer.save()
        except DatabaseError as error:
            print("Error:\n", error)
            return get_status_response('Database Error')
    responce = {'url': url, 'msg': STATUS_CODE['Success']}
    return JsonResponse(responce)


@login_required
@require_http_methods(['POST'])
def get_sellrecords(request):
    """
    本api用于地推人员本人查看自己业绩

    :url: api/get_sellrecords

    :前端传入数据样例: data = {'username': 'username', 'date0': '2018-08-08',

    'date1': '2018-08-31'}

    :返回: 今日销售数量、今日销售收入、所选日期销售数量、所选日期销售收入

    :返回值: Json字典

    :返回样例: {'list': [{'today_count': '2', 'today_money': '69.96',

    'history_count': '2', 'history_money': '69.96'}]}
    """
    response = {}
    list_this = []
    temp_dict = {}
    data = json.loads(request.body)
    seller_name = data['username']
    start = data['date0']
    end = data['date1']
    today = datetime.now()
    tomorrow = today + timedelta(hours=23, minutes=59, seconds=59)
    today = today.strftime("%Y-%m-%d")
    tomorrow = tomorrow.strftime("%Y-%m-%d")
    seller = User.objects.filter(username=seller_name)
    seller_info = SellerInfo.objects.filter(seller=seller[0])
    to_sellrecords = SellRecord.objects.filter(
        seller=seller_info[0], date__range=[today, tomorrow])
    temp_dict['today_count'] = str(to_sellrecords.count())
    temp_dict['today_money'] = str(round(get_records_money(to_sellrecords), 2))
    if start is None or end is None:
        result = create_timedelta(start, end)
        start = result['start']
        end = result['end']
    his_sellrecords = SellRecord.objects.filter(
        seller=seller_info[0], date__range=[start, end])
    temp_dict['history_count'] = str(his_sellrecords.count())
    temp_dict['history_money'] = str(
        round(get_records_money(his_sellrecords), 2))
    list_this.append(temp_dict)
    response['list'] = list_this
    return JsonResponse(response)


def get_ccrecords(username, date_from, date_to) -> tuple:
    '''根据时间返回课程顾问业绩'''
    result = {}
    try:
        user = User.objects.get(
            username=username, user_type=USER_TYPE['consultant'])
    except User.DoedNotExist:
        return (STATUS_CODE['User Not Found'], [])
    customers = user.cc_customers.filter(
        date_cc__range=[date_from, date_to])
    flow_num = len(customers)
    audition_num = flow_num - len(customers.filter(audition_count=0))
    audition_rate = (
        '0%' if flow_num == 0 else format(audition_num/flow_num, '.0%'))
    consumption_num = len(customers.filter(is_signedup=True))
    consumption_rate = (
        '0%' if audition_num == 0
        else format(consumption_num/audition_num, '.0%')
    )
    flow_change_rate = (
        '0%' if flow_num == 0 else format(consumption_num/flow_num, '.0%'))
    cc_records = user.sell_record.filter(
        date__range=[date_from, date_to])
    income = 0.0
    for record in cc_records:
        income = income + record.money
    result['flow_num'] = flow_num
    result['audition_num'] = audition_num
    result['audition_rate'] = audition_rate
    result['consumption_num'] = consumption_num
    result['consumption_rate'] = consumption_rate
    result['flow_change_rate'] = flow_change_rate
    result['income'] = income
    return (STATUS_CODE['Success'], result)


@login_required
@require_http_methods(['POST'])
def view_ccrecords(request):
    '''处理查看课程顾问销售业绩的请求'''
    respose = {}
    data = json.loads(request.body)
    username = ''
    if 'username' in data:
        username = data['username']
    else:
        username = request.user.username
    if 'date_from' in data and 'date_to' in data:
        date_from = data['date_from']
        date_to = data['date_to']
        if date_from is None or date_to is None:
            time_this = create_timedelta(date_from, date_to)
            date_from = time_this['start']
            date_to = time_this['end']
        results = get_ccrecords(username, date_from, date_to)
        respose['msg'] = results[0]
        respose['list'] = results[1]
    else:
        respose['msg'] = STATUS_CODE['Error Time Range']
        respose['list'] = []
    return JsonResponse(respose)


def course_by_student(tel: str, childname: str):
    """
    本函数用于返回该学生的课程信息

    :接收参数: tel(string)电话号码 childname(string)学生姓名

    :返回: 该学生的课程信息或0(用户不存在)
    """
    user = User.objects.filter(username=tel)
    if user.count() == 0:
        return 0
    customer = Customer.objects.filter(user=user[0], child_name=childname)
    if customer.count() == 0:
        return 0
    customer = customer[0]
    return customer.takes.all()


def course_by_teacher(teacher_name: str, be_courses):
    """
    本函数用于返回该老师所教的课程信息

    :接收参数: teacher_name(string)老师姓名 be_courses(课程对象集合)

    :返回: 该老师的课程信息或0(无符合条件的结果)
    """
    teacher = Teacher.objects.filter(name=teacher_name)
    if teacher.count() == 0:
        return 0
    courses = be_courses.filter(teacher_id=teacher[0])
    return courses


def deal_with_courses(courses):
    """
    本函数用于补充额外的课程信息: 老师姓名, 学生人数, 目前课节

    :接收参数: courses(课程对象集合)

    :返回: 该老师的课程信息或0(无符合条件的结果)
    """
    course_list = []
    for temp_dict in courses:
        teacher = Teacher.objects.filter(pk=temp_dict['teacher_id_id'])
        temp_dict['teacher'] = teacher[0].name
        temp_course = Courses.objects.filter(pk=temp_dict['id'])[0]
        temp_dict['num'] = len(temp_course.taken.all())
        count = 0
        temp_dict['sections'] = list(temp_course.sections.all().values())
        for section in temp_course.sections.all():
            if date.today() >= section.date:
                count = section.count
        temp_dict['cur_sec'] = count
        course_list.append(temp_dict)
    return course_list


@login_required
@require_http_methods(['POST'])
def eduadmin_get_courses(request):
    """
    本api用于教务老师按条件搜索获得相应课程信息

    :url: api/eduadmin_get_courses

    :前端传入数据: data = {'tel': '15912340711', 'childname': 'name',

    'teacher': 'teacher_name', 'day': '1', 'time': '08:00'}

    :返回: error状态码和课程信息列表

    :返回值: Json字典

    :返回样例: {'error': 0, 'list': [{'id': 1, 'name': 'course1',

    'teacher_id_id': 1, 'time': '08:00:00', 'date': 1, 'time_length': 120,

    'total_sec': 48, 'price': None, 'teacher': 'teacher1', 'num': 2,

    'cur_sec': 4}]}

    :状态码解释: 0(操作成功) 1(没有符合条件的搜索结果)
    """
    response = {}
    data = json.loads(request.body)
    tel = data['tel']
    childname = data['childname']
    teacher = data['teacher']
    date_this = data['day']
    time_this = data['time']
    courses = Courses.objects.filter()
    if tel != '' and childname != '':
        courses = course_by_student(tel, childname)
        if courses == 0:
            response['error'] = STATUS_CODE['Not Found']
            return JsonResponse(response)
    if teacher != '':
        courses = course_by_teacher(teacher, courses)
        if courses == 0:
            response['error'] = STATUS_CODE['Not Found']
            return JsonResponse(response)
    if date_this != '':
        date_this = int(date_this)
        courses = courses.filter(date=date_this)
        if courses == 0:
            response['error'] = STATUS_CODE['Not Found']
            return JsonResponse(response)
    if time_this != '':
        courses = courses.filter(time=time_this)
        if courses == 0:
            response['error'] = STATUS_CODE['Not Found']
            return JsonResponse(response)
    response['error'] = STATUS_CODE['Success']
    response['list'] = deal_with_courses(list(courses.values()))
    response['teachers'] = get_teacher_info()['list']
    return JsonResponse(response)


@login_required
@require_http_methods(['POST'])
def eduadmin_cancell_courses(request):
    """
    本api用于教务老师查看近一周已销课情况和所有未销课情况

    :url: api/eduadmin_cancell_courses

    :返回: 销课信息数量和相应的具体信息

    :返回值: Json字典

    :返回样例: {'count': 2, 'list': [{'id': 6, 'course_id_id': 2, 'count': 2,

    'name': 'course1(2)', 'date': '2018-08-06', 'start_time': '08:00:00',

    'end_time': '10:00:00', 'location': '5A', 'is_cancel': False},

    {'id': 8, 'course_id_id': 2, 'count': 4, 'name': 'course1(4)',

    'date': '2018-08-20', 'start_time': '08:00:00', 'end_time': '10:00:00',

    'location': '5A', 'is_cancel': False}]}
    """
    response = {}
    sections = Section.objects.filter(date__lte=date.today())
    sections = sections.exclude(
        date__lt=date.today()-timedelta(hours=24*7), is_cancel=True)
    if sections.count() == 0:
        response['count'] = 0
        return JsonResponse(response)
    response['count'] = sections.count()
    for section in sections.filter():
        if section.name is None and section.count != 0:
            course_name = Courses.objects.get(pk=section.course_id_id).name
            temp_sec = Section.objects.get(pk=section.id)
            temp_sec.name = course_name + '(' + str(section.count) + ')'
            temp_sec.save()
    response['list'] = list(sections.values())
    return JsonResponse(response)


@login_required
@require_http_methods(['POST'])
def eduadmin_ensure_cancell(request):
    """
    本api用于教务老师确认销课

    :url: api/eduadmin_ensure_cancell

    :前端传入数据:  data = {'id': 1(课节id)}

    :返回: 是否成功的标识

    :返回值: json字典

    :返回样例(成功): {'seccess': True}
    """
    response = {}
    data = json.loads(request.body)
    section = Section.objects.get(pk=data['id'])
    try:
        section.is_cancel = True
        section.save()
    except Section.DoesNotExist:
        response['seccess'] = False
        return JsonResponse(response)
    response['seccess'] = True
    return JsonResponse(response)


@login_required
@require_http_methods(['POST'])
def eduadmin_arrange_course(request):
    """
    本api用于教务老师给学生安排课程

    :url: api/change_section_info

    :前端传入数据: data = {'id': 1(课程id), 'tel': '15912340711'(家长电话号码),

    'child_name': 'childname'}

    :返回: error状态码

    :返回值: Json字典

    :返回样例: {'error': 0}

    :状态码解释: 0(操作成功) 1(传入信息不正确)
    """
    response = {}
    data = json.loads(request.body)
    course_id = data['id']
    tel = data['tel']
    child_name = data['child_name']
    if User.objects.filter(username=tel).count() == 0:
        response['error'] = STATUS_CODE['Not Found']
        return JsonResponse(response)
    user_id = User.objects.get(username=tel).id
    if Customer.objects.filter(
            user_id=user_id, child_name=child_name).count() == 0:
        response['error'] = STATUS_CODE['Not Found']
        return JsonResponse(response)
    customer = Customer.objects.get(user_id=user_id, child_name=child_name)
    for take in customer.takes.all():
        if take.id == course_id:
            response['error'] = STATUS_CODE['Not Found']
            return JsonResponse(response)
    course = Courses.objects.get(pk=course_id)
    cc_record = CcRecord.objects.filter(customer=customer, course=None)
    if cc_record.count() == 0:
        response['error'] = STATUS_CODE['Not Found']
        return JsonResponse(response)
    cc_record = CcRecord.objects.get(customer=customer, course=None)
    cc_record.course = course
    cc_record.save()
    response['error'] = STATUS_CODE['Success']
    return JsonResponse(response)


@login_required
@require_http_methods(['POST'])
def eduadmin_check_refund(request):
    '''
    教务老师查看退款信息

    :url: eduadmin_check_refund

    :前端传入数据: data: {'course_message': '围棋'(课程搜索关键字)}

    :返回: 退款记录、顾客信息、课程信息

    :返回值: Json字典

    :返回样例: 

    '''
    response = {}
    data = json.loads(request.body)
    courses = None
    if 'course_message' in data:
        msg = data['course_message']
        courses = Courses.objects.filter(
            Q(name__icontains=msg) | Q(id__icontains=msg))
        courses_id = courses.values_list('id', flat=True)
    if courses:
        refund_records = RefundRecord.objects.filter(
            course__in=courses_id, is_paid=False)
    else:
        refund_records = RefundRecord.objects.filter(is_paid=False)
        courses = Courses.objects.all()
    if refund_records.count() == 0 or courses.count() == 0:
        response['msg'] = STATUS_CODE['Trade Record Exception']
        return JsonResponse(response)
    customers_id = refund_records.values_list("customer_id", flat=True)
    customers = Customer.objects.filter(id__in=customers_id)
    response['msg'] = STATUS_CODE['Success']
    response['refund_records'] = serialize("json", refund_records)
    response['customers'] = serialize("json", customers)
    response['courses'] = serialize("json", courses)
    print(response)
    return JsonResponse(response)


def check_front_key_exists(data: dict, require_keys: tuple) -> bool:
    '''
    检查前端数据是否异常

    :参数: data 为从前端 json 数据中提取出的数据, require_key 为需要保证存在的键的集合

    :返回数据: bool 如果需要的键全部存在返回 True, 否则返回 False

    '''
    for key in require_keys:
        if key not in data:
            return False
    return True


def check_data_of_eduamdin(data):
    """
    获取教务页面传来的信息

    :传入参数: 从前端传回来的 json 请求进行解码后的字典

    :返回数据: 如果参数不全, 返回装有"前端数据异常"的 JsonResponse 响应, 否则为 None

    """
    response = {}
    if check_front_key_exists(data, ('customer_id', 'course_id')):
        response['msg'] = STATUS_CODE['Frontend Value Error']
        return JsonResponse(response)
    return None


def get_status_response(msg):
    """
    获取状态码并包装为 JsonResponse 响应

    :传入参数: 状态码搜索的键

    :返回数据: 包装有状态码的 JsonResponse 响应

    """
    response = {'msg': STATUS_CODE[msg]}
    return JsonResponse(response)


def get_refund_response(msg):
    '''
    返回退款状态码

    :传入参数: 退款信息

    :返回: 退款信息状态码

    '''
    response = {'msg': REFUND_STATUS[msg]}
    return JsonResponse(response)


def get_customer(customer_id):
    '''获得家长类的一行'''
    customer = Customer.objects.filter(id=customer_id)
    if not customer.exists():
        return None
    return customer.first()


@login_required
@require_http_methods(['POST'])
def eduadmin_ensure_refund(request):
    '''
    教务老师最终确认退课，退款进入用户账户

    :url: api/eduadmin_ensure_refund

    :传入参数: 顾客 id、课程 id

    :返回: 状态码

    :返回样例: {'msg': 0} 状态码含义具体请参考 statuscode.py 文件

    '''
    data = json.loads(request.body)
    if not check_front_key_exists(data, ('customer_id', 'course_id')):
        return get_status_response('Frontend Value Error')
    refund_records = RefundRecord.objects.filter(
        customer__id=data['customer_id'], course__id=data['course_id'])
    if not refund_records.exists():
        return get_status_response('Refund Record Exception')
    refund_record = refund_records.first()
    if not refund_record.is_passed:
        return get_refund_response('Under Review')
    if refund_record.is_paid:
        return get_refund_response('Already Paid')
    ccrecord = CcRecord.objects.filter(
        customer__id=data['customer_id'], course__id=data['course_id'])
    if not ccrecord.exists():
        return get_status_response('Trade Record Exception')
    price = ccrecord.first().money
    trade_no = ccrecord.first().trade_no
    print(trade_no)
    amount = price if 'refund_account' not in data else data['refund_account']
    if amount > price:
        return get_status_response('Price Not Match')
    trade_result = solve_trade(
        TRADE_TYPE['refund'], trade_no=trade_no, amount=amount)
    print(trade_result)
    if not trade_result:
        return get_status_response('Alipay Error')
    refund_record.is_paid = True
    refund_record.save()
    response = {'msg': STATUS_CODE['Succees']}
    customer = get_customer(data['customer_id'])
    if not customer:
        return get_status_response('Customer Not Found')
    OperationLogs.objects.create(
        operator=request.user, type=0, username=customer.child_name,
        info=request.user.username + '确认退款给' +
        customer.child_name + '家长' + str(amount) + '元')
    return JsonResponse(response)


def get_cancel_num(course, date_this):
    """
    本函数用于获得该课的相应日期内的销课次数

    :传入参数: course(课程实例对象) date(date()实例对象)

    :返回: 销课次数
    """
    count = 0
    for section in course.sections.filter(date__lte=date_this, is_cancel=True):
        if section.count > count:
            count = section.count
    return count


def add_info_records(records):
    """
    本api用于补充额外的退费申请信息

    :传入参数: records(退费申请集合)

    :返回: 退费申请的详细信息

    :返回值: 列表
    """
    rec_list = []
    for temp_dict in records:
        customer = Customer.objects.get(pk=temp_dict.pop('customer_id'))
        temp_dict['phone'] = customer.user.username
        temp_dict['stu_name'] = customer.child_name
        temp_dict['date'] = temp_dict.pop('date').strftime("%Y-%m-%d")
        date_this = datetime.strptime(temp_dict['date'], '%Y-%m-%d')
        course_id = temp_dict['course_id']
        course = Courses.objects.get(pk=course_id)
        temp_dict['coursename'] = course.name
        temp_dict['total_sec'] = course.total_sec
        cc = User.objects.get(pk=temp_dict['cc_id'])
        cc_record = CcRecord.objects.get(
            customer=customer, cc=cc, course=course)
        if not temp_dict['is_passed']:
            del temp_dict['deal_date']
            del temp_dict['refund']
        else:
            temp_dict['date1'] = temp_dict.pop(
                'deal_date').strftime("%Y-%m-%d")
            del temp_dict['reason']
        temp_dict['payment'] = cc_record.money
        temp_dict['cncl_num'] = get_cancel_num(course, date_this)
        del temp_dict['is_passed']
        del temp_dict['cc_id']
        rec_list.append(temp_dict)
    return rec_list


@login_required
@require_http_methods(['POST'])
def cc_check_refund(request):
    """
    本api用于课程顾问查看退款信息

    :url: api/cc_check_refund

    :前端传入数据: data = {'username': 'consultant_name',

    'refund': True(查看已退款的信息)}

    :返回: 已退款的信息记录

    :返回值: json字典

    :返回样例: {'list': [{'id': 2, 'course_id': 2, 'is_paid': False,

    'reason': 'the time does not fit', 'phone': '15900001234',

    'stu_name': 'child1', 'date': '2018-08-07', 'coursename': 'course2',

    'total_sec': 48, 'payment': 6696.0, 'cncl_num': 19}]}
    """
    response = {}
    data = json.loads(request.body)
    cc_name = data['username']
    refund = data['refund']
    cc = User.objects.get(username=cc_name)
    if refund:
        monago = datetime.now() - timedelta(hours=24*30)
        records = RefundRecord.objects.filter(
            deal_date__gte=monago, is_passed=True, cc=cc)
        if records.count() == 0:
            response['count'] = 0
            return JsonResponse(response)
        records = add_info_records(list(records.values()))
    else:
        records = RefundRecord.objects.filter(is_passed=False, cc=cc)
        if records.count() == 0:
            response['count'] = 0
            return JsonResponse(response)
        records = add_info_records(list(records.values()))
    response['list'] = records
    return JsonResponse(response)


@login_required
@require_http_methods(['POST'])
def cc_ensure_refund(request):
    """
    本api用于课程顾问同意并填写退款金额

    :url: api/cc_ensure_refund

    :前端传入数据: data = {'id': 8(退款记录的id), 'refund': '2500'(退款金额)}

    :返回: error状态码

    :返回值: Json字典

    :返回样例: {'error': 0}

    :状态码解释: 0(操作成功) 1(退款记录不存在)
    """
    response = {}
    data = json.loads(request.body)
    refund = data['refund']
    if RefundRecord.objects.filter(pk=data['id']).count() == 0:
        response['error'] = STATUS_CODE['Not Found']
        return JsonResponse(response)
    record = RefundRecord.objects.get(pk=data['id'])
    record.is_passed = True
    record.refund = float(refund)
    record.save()
    response['error'] = STATUS_CODE['Success']
    return JsonResponse(response)


@login_required
@require_http_methods(['POST'])
def cc_signup_info(request):
    """
    本api用于课程顾问填写报名信息进行正式课报名

    :url: api/cc_signup_info

    :前端传入数据: data = {'tel': '17750126548', 'child_name': 'child',

    'parent_name': 'parent', 'classin_id': '123456', 'classin_name': 'name',

    'birthday': '2011-11-11', 'old_user': '13801231111', 'money': '2999.9',

    'day1': '星期五', 'time1': '08:00:00', 'day2': '星期六',

    'time2': '10:00:00', 'day3': '星期日', 'time3': '14:00:00'(顾客意愿时间),

    'demand': '少儿班'(顾客需求)}

    :返回: error状态码

    :返回值: Json字典

    :返回样例: {'error': 0}

    :状态码解释: 0(操作成功) 902(用户信息不存在) 907(学生信息不存在)

    805(有待支付的课程) 908(老客户不存在)
    """
    response = {}
    data = json.loads(request.body)
    user = User.objects.filter(username=data['tel'])
    if user.count() == 0:
        response['error'] = STATUS_CODE['User Not Found']
        return JsonResponse(response)
    user = User.objects.get(username=data['tel'])
    customer = Customer.objects.filter(
        user=user, child_name=data['child_name'])
    if customer.count() == 0:
        response['error'] = STATUS_CODE['Child Not Found']
        return JsonResponse(response)
    customer = Customer.objects.get(
        user=user, child_name=data['child_name'])
    if CcRecord.objects.filter(customer=customer, course=None).exists():
        response['error'] = STATUS_CODE['Course Not Paid']
        return JsonResponse(response)
    customer.parent_name = data['parent_name']
    customer.classin_id = data['classin_id']
    customer.classin_id = data['classin_name']
    customer.birthday = data['birthday']
    if data['old_user'] != "":
        if User.objects.filter(username=data['old_user']).count() == 0:
            response['error'] = STATUS_CODE['Old Not Found']
            return JsonResponse(response)
        old_user = User.objects.get(username=data['old_user'])
        customer.old_user = Customer.objects.get(user=old_user)
    customer.demand = ('时间：' + data['day1'] +
                       data['time1'] + " " + data['day2'] +
                       data['time2'] + " " + data['day3'] +
                       data['time3'] + " 课程要求： " + data['demand'])
    trade_no = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
    trade_no += ''.join([str(random.randint(0, 9)) for i in range(0, 5)])
    CcRecord.objects.create(
        customer=customer, cc=request.user,
        trade_no=trade_no, money=float(data['money']))
    customer.save()
    response['error'] = STATUS_CODE['Success']
    return JsonResponse(response)


@login_required
@require_http_methods(['POST'])
def superuser_register(request):
    """
    本api用于超级管理员注册员工

    :url: api/superuser_register

    :前端传入数据: data = {'username': 'eduadmin', 'password': 'eduadmin',

    'user_type': USER_TYPE['eduadmin'], 'gender': 'woman',

    'email': '123456789@qq.com'}

    :返回: error状态码

    :返回值: Json字典

    :返回样例: {'error': 0}

    :状态码解释: 0(操作成功) 909(用户已存在)
    """
    response = {}
    data = json.loads(request.body)
    username = data['username']
    password = data['password']
    user_type = int(data['user_type'])
    email = data['email']
    gender = data['gender']
    if User.objects.filter(username=username).count() != 0:
        response['error'] = STATUS_CODE['User Already Exists']
        return JsonResponse(response)
    if gender == 'man':
        gender = 'male'
    else:
        gender = 'female'
    user = User.objects.create(
        username=username, user_type=user_type, gender=gender, email=email)
    user.set_password(password)
    user.save()
    if user_type == USER_TYPE['seller']:
        city = data['city']
        price = float(data['price'])
        SellerInfo.objects.create(seller=user, city=city, price=price)
    operator = request.user
    OperationLogs.objects.create(
        operator=operator, type=LOG_TYPE['Add User'], username=username,
        info=operator.username+'注册了员工'+username)
    response['error'] = STATUS_CODE['Success']
    return JsonResponse(response)


@login_required
@require_http_methods(['POST'])
def superuser_import_customer(request):
    """
    本api用于处理超级管理员导入客户

    :前端发送数据: FormData 包含文件

    :url: data/sup_import_customer

    :返回类型: msg: 状态码 error 错误列表

    :返回格式: {'msg': 0, 'error': [{'msg': 705, 'name': '1234567890'}]}

    """
    response = {}
    thefile = request.FILES.get('file')
    if thefile:
        path = os.path.join('document/', thefile.name)
        file_in = default_storage.save(path, ContentFile(thefile.read()))
    else:
        response['msg'] = STATUS_CODE['Frontend Value Error']
        response['error'] = []
        return JsonResponse(response)
    if request.user.user_type == USER_TYPE['superuser']:
        result = import_customer_info(
            file_in,
            thefile.name,
            request.user
        )
        response['msg'] = result[0]
        response['error'] = result[1]
    else:
        response['msg'] = STATUS_CODE['Identity Error']
        response['error'] = STATUS_CODE['Identity Error']
    os.remove(path)
    return JsonResponse(response)


@login_required
@require_http_methods(['POST'])
def superuser_modify_user(request):
    """
    本api用于修改用户信息

    :url: api/modify_user

    :前端传入信息: username(用户名) form(修改信息字典)

    :返回: 状态码 0或901

    """
    data = json.loads(request.body)
    response = {}
    if request.user.user_type == USER_TYPE['superuser']:
        response['msg'] = modify_user_info(data['username'], data)
    else:
        response['msg'] = STATUS_CODE['Identity Error']
    return JsonResponse(response)


@login_required
@require_http_methods(['POST'])
def superuser_modify_customer(request):
    """
    本api用于修改家长信息

    :url: api/modify_customer

    :前端传入信息: customer_id form(修改信息字典)

    :返回: 状态码 0或901或902

    """
    data = json.loads(request.body)
    response = {}
    if request.user.user_type == USER_TYPE['superuser']:
        response['msg'] = modify_customer_info(data['customer_id'], data)
    else:
        response['msg'] = STATUS_CODE['Identity Error']
    return JsonResponse(response)


@login_required
@require_http_methods(['POST'])
def superuser_view_users(request):
    """
    本api用于处理超级管理员查看用户信息的请求

    :url: api/sup_view_users

    :前端传入数据: username user_type

    :返回数据: 'msg' 状态码 0或901; 'list'  [dict] 用户信息

    :返回字典键值: id , password, last_login, is_superuser, username,

    first_name, last_name, email, is_staff, is_active, date_joined,

    user_type, gender

    """
    data = json.loads(request.body)
    response = {}
    if request.user.user_type == USER_TYPE['superuser']:
        username = (
            '' if 'username' not in data else data['username'])
        user_type = (
            USER_TYPE['customer'] if 'user_type' not in data
            else data['user_type'])
        response['list'] = search_user_info(username, user_type)
        response['msg'] = STATUS_CODE['Success']
    else:
        response['list'] = []
        response['msg'] = STATUS_CODE['Identity Error']
    return JsonResponse(response)


@login_required
@require_http_methods(['POST'])
def superuser_view_customers(request):
    """
    本api用于处理超级管理员查看客户信息的请求

    :url: api/sup_view_customers

    :前端传入数据: username

    :返回数据: 'msg' 状态码 0或901; 'list' :客户信息 字典

    :返回样例： [{'id': 5, 'user_id': 7, 'child_name': 'child1',

                'parent_name': None, 'classin_id': None,

                'classin_name': None, 'birthday': None,

                'cc_id': 'consultant', 'audition_count': 0,

                'is_signedup': False, 'is_paid': True,

                'old_user_id': None, 'date_cc': None,

                'demand': None, 'gender': None}

    """
    data = json.loads(request.body)
    response = {}
    if request.user.user_type == USER_TYPE['superuser']:
        response['list'] = get_info(data['username'])
        response['msg'] = STATUS_CODE['Success']
    else:
        response['list'] = []
        response['msg'] = STATUS_CODE['Identity Error']
    return JsonResponse(response)


@login_required
@require_http_methods(['POST'])
def superuser_delete_customer(request):
    """
    本api用于处理超级管理员删除客户的请求

    :url: api/delete_customer

    :前端传入数据: customer_id

    :返回数据: 状态码 0或904或901或705

    """
    data = json.loads(request.body)
    response = {}
    if request.user.user_type == USER_TYPE['superuser']:
        if 'customer_id' in data:
            try:
                customer = Customer.objects.get(id=data['customer_id'])
                OperationLogs.objects.create(
                    operator=request.user,
                    type=LOG_TYPE['Delete Customer'],
                    username=customer.child_name,
                    info='deleted'
                ).save()
                customer.delete()
            except Customer.DoesNotExist:
                response['msg'] = STATUS_CODE['Customer Not Found']
            response['msg'] = STATUS_CODE['Success']
        else:
            response['msg'] = STATUS_CODE['Frontend Value Error']
    else:
        response['msg'] = STATUS_CODE['Identity Error']
    return JsonResponse(response)


@login_required
@require_http_methods(['POST'])
def superuser_delete_user(request):
    """
    本api用于处理超级管理员删除用户的请求

    :url: api/delete_user

    :前端传入数据: username

    :返回数据: 状态码 0或902或901或705

    """
    data = json.loads(request.body)
    response = {}
    if request.user.user_type == USER_TYPE['superuser']:
        if 'username' in data:
            try:
                user = User.objects.get(username=data['username'])
                OperationLogs.objects.create(
                    operator=request.user,
                    type=LOG_TYPE['Delete User'],
                    username=user.username,
                    info='deleted'
                ).save()
                user.delete()
            except User.DoesNotExist:
                response['msg'] = STATUS_CODE['User Not Found']
            response['msg'] = STATUS_CODE['Success']
        else:
            response['msg'] = STATUS_CODE['Frontend Value Error']
    else:
        response['msg'] = STATUS_CODE['Identity Error']
    return JsonResponse(response)


@login_required
@require_http_methods(['POST'])
def cc_view_customers(request):
    """
    本api用于处理课程顾问查看用户的请求

    :url: api/cc_view_customers

    :前端传入数据: 无,需登陆

    :返回数据: msg: 0或901 list: 用户数据列表

    :返回样例: {'list': [{'id': 1, tel': '12345678910', 'child_name':

            'child2', 'parent_name': None, 'audition_count': 2,

            'is_signedup': True}, {'id': 2, 'tel': '12345678911',

            'child_name': 'child1', 'parent_name': None,

            'audition_count': 1, 'is_signedup': True},

            {'id': 1, 'tel': '12345678912', 'child_name': 'child0',

            'parent_name': None, 'audition_count': 0,

            'is_signedup': False}], 'msg': 0}
    """
    cc_this = request.user
    response = {}
    response['list'] = []
    if request.user.user_type == USER_TYPE['consultant']:
        customers = cc_this.cc_customers.filter().order_by('-date_cc')
        for customer in customers:
            result = {}
            result['id'] = customer.id
            result['tel'] = customer.user.username
            result['child_name'] = customer.child_name
            result['parent_name'] = customer.parent_name
            result['audition_count'] = customer.audition_count
            result['is_signedup'] = customer.is_signedup
            response['list'].append(result)
        response['msg'] = STATUS_CODE['Success']
    else:
        response['msg'] = STATUS_CODE['Identity Error']
    return JsonResponse(response)
