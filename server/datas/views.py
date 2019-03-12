# -*- coding: utf-8 -*-

'''本文件用于实现数据可视化 api 接口'''

import json
import os
from datetime import date, datetime, timedelta

from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from courses.models import Teacher, Section
from customers.models import Customer
from statuscode import STATUS_CODE, USER_TYPE
from users.models import User

from .models import (AuditionRecord, CcRecord, SellerInfo,
                     SellRecord, import_courses)


@login_required
@require_http_methods(['POST'])
def today_grades(request):
    """
    本函数用于获取今日试听人数、试听收入、报名人数、报名收入

    :url: data/today_grades

    :返回: 试听人数、注册试听收入、报名人数、报名收入

    :返回值: Json字典

    :返回样例: {'audition_count': 3, 'audition_income': 89.6999,

    'entered_count': 3, 'entered_income': 8999.7}
    """
    response = {}
    today = datetime.now()
    tomorrow = today + timedelta(hours=23, minutes=59, seconds=59)
    today = today.strftime("%Y-%m-%d")
    tomorrow = tomorrow.strftime("%Y-%m-%d")
    records = AuditionRecord.objects.filter(date__range=[today, tomorrow])
    response['audition_count'] = records.count()
    if records.count() == 0:
        response['audition_income'] = round(0, 2)
    else:
        income = 0.0
        for record in records:
            customer = record.customer
            money = SellRecord.objects.get(customer=customer).money
            income += money
        response['audition_income'] = round(income, 2)
    ccrecords = CcRecord.objects.filter(
        date__range=[today, tomorrow], is_paid=True)
    response['entered_count'] = ccrecords.count()
    if ccrecords.count() == 0:
        response['entered_count'] = 0
        response['entered_income'] = round(0, 2)
        return JsonResponse(response)
    income = 0.0
    for ccrecord in ccrecords:
        income += ccrecord.money
    response['entered_income'] = round(income, 2)
    return JsonResponse(response)


def get_records_money(records):
    """
    本函数用于获取获取参数列表中'money'字段数值总和

    :传入参数: 带有数值'money'属性的对象列表

    :返回: 总金额
    """
    money = 0.0
    for record in records:
        money += record.money
    return money


def get_indate_sell_grades(name, start, end):
    """
    本函数获得地推人员相应时间内注册试听人数、金额及后续报名人数、金额

    :传入参数: name(string)地推人员姓名，为空的时候代表全体

    start, end(string)%Y-%m-%d格式的日期字符串

    :返回: 地推人员相应时间内注册试听人数、金额及后续报名人数、金额

    :返回值: 字典
    """
    response = {}
    if name == "":
        sellrecords = SellRecord.objects.filter(date__range=[start, end])
        response['sellcount'] = sellrecords.count()
        response['sellmoney'] = round(get_records_money(sellrecords), 2)
        ccrecords = CcRecord.objects.filter(date__range=[start, end])
        response['signcount'] = ccrecords.count()
        response['signmoney'] = round(get_records_money(ccrecords), 2)
        response['error'] = STATUS_CODE['Success']
        return response
    sell_user = User.objects.filter(
        username=name, user_type=USER_TYPE['seller'])
    if sell_user.count() == 0:
        response['error'] = STATUS_CODE['Not Found']
        return response
    sell_user = User.objects.get(
        username=name, user_type=USER_TYPE['seller'])
    seller_info = SellerInfo.objects.get(seller=sell_user)
    sellrecords = seller_info.sell_record.filter(date__range=[start, end])
    response['sellcount'] = sellrecords.count()
    response['sellmoney'] = round(get_records_money(sellrecords), 2)
    sellrecords = SellRecord.objects.filter(seller=seller_info)
    count = 0
    money = 0.0
    for sellrecord in sellrecords:
        customer = sellrecord.customer
        signrecords = customer.signup_record.filter(
            date__range=[start, end], is_paid=True)
        count += signrecords.count()
        money += float(get_records_money(signrecords))
    response['signcount'] = count
    response['signmoney'] = round(money, 2)
    response['error'] = STATUS_CODE['Success']
    return response


@login_required
@require_http_methods(['POST'])
def today_seller_grades(request):
    """
    本api用于获取今天地推人员的业绩

    :url: data/today_seller_grades

    :前端传送数据: {'name': 'name'(为空时代表全体地推人员)}

    :返回: error状态码和业绩信息

    :返回值: Json字典

    :返回样例(成功返回): {'error': 0, 'today_sellcount': 3,

    'today_sellmoney': 89.6999, 'today_signcount': 3,

    'today_signmoney': 8999.7}

    :返回样例(用户名不存在): {'error': 0}
    """
    response = {}
    data = json.loads(request.body)
    name = data['name']
    today = datetime.now()
    tomorrow = today + timedelta(hours=23, minutes=59, seconds=59)
    today = today.strftime("%Y-%m-%d")
    tomorrow = tomorrow.strftime("%Y-%m-%d")
    temp_response = get_indate_sell_grades(name, today, tomorrow)
    response['error'] = temp_response['error']
    print(response['error'])
    if response['error'] == STATUS_CODE['Not Found']:
        return JsonResponse(response)
    response['today_sellcount'] = temp_response['sellcount']
    response['today_sellmoney'] = temp_response['sellmoney']
    response['today_signcount'] = temp_response['signcount']
    response['today_signmoney'] = temp_response['signmoney']
    return JsonResponse(response)


def get_seller_rate(name, start, end):
    """
    本函数用来根据时间和名字返回地推的转化率

    :传入参数: name(string)地推人员姓名，为空的时候代表全体

    start, end(string)%Y-%m-%d格式的日期字符串

    :返回: 地推人员相应时间内注册试听人数, 金额及后续报名人数, 金额以及相应的转化率
    """
    response = get_indate_sell_grades(name, start, end)
    if response['error'] == STATUS_CODE['Not Found']:
        return response
    if name == '':
        count = AuditionRecord.objects.filter(date__range=[start, end]).count()
        response['auditioncount'] = count
    else:
        seller = User.objects.get(username=name)
        sellerinfo = SellerInfo.objects.get(seller=seller)
        sellrecords = sellerinfo.sell_record.filter()
        count = 0
        for sellrecord in sellrecords:
            customer = sellrecord.customer
            count += customer.audition_record.filter(
                date__range=[start, end]).count()
        response['auditioncount'] = count
    if response['sellcount'] == 0:
        response['audition_rate'] = 0
    else:
        response['audition_rate'] = round(count/response['sellcount'], 2)*100
    if count == 0:
        response['sign_rate'] = 0
    else:
        response['sign_rate'] = round(response['signcount']/count, 2)*100
    response['date'] = start
    return response


@login_required
@require_http_methods(['POST'])
def week_seller_grades(request):
    """
    本api获得最近七天内地推人员业绩可视化数据来源

    :url: data/week_seller_grades

    :前端传送数据: {'name': 'name'(为空时代表全体地推人员)}

    :返回: 最近七天地推人员销售数量、销售收入、试听率、转化率

    :返回值: Json字典

    :返回样例(七天中的一天): {'list': [{'sellcount': 0, 'sellmoney': 0.0,

    'signcount': 0, 'signmoney': 0.0, 'error': 0, 'auditioncount': 0,

    'audition_rate': 0, 'sign_rate': 0, 'date': '2018-08-22'} ··· ··· ]}

    :返回样例(用户名不存在): {'list': [{'error': 1}, {'error': 1}, {'error': 1},

    {'error': 1}, {'error': 1}, {'error': 1}, {'error': 1}]}
    """
    response = {}
    res_list = []
    data = json.loads(request.body)
    name = data['name']
    today = datetime.now()
    start = today - timedelta(hours=24*6)
    for _ in range(7):
        end = start + timedelta(hours=23, minutes=59, seconds=59)
        res_list.append(get_seller_rate(name, start.strftime(
            "%Y-%m-%d"), end.strftime("%Y-%m-%d")))
        start = end
    response['list'] = res_list
    return JsonResponse(response)


@login_required
@require_http_methods(['POST'])
def months_seller_grades(request):
    """
    本api获得今年各月销售人员业绩可视化数据来源

    :url: data/months_seller_grades

    :前端传送数据: {'name': 'name'(为空时代表全体地推人员)}

    :返回: 今年12个月地推人员销售数量、销售收入、试听率、转化率

    :返回值: Json字典

    :返回样例(只显示一个月样例): {'list': [{'sellcount': 1, 'sellmoney': 29.9,

    'signcount': 1, 'signmoney': 2999.9, 'error': 0, 'auditioncount': 1,

    'audition_rate': 100.0, 'sign_rate': 100.0} ··· ··· ]}

    :返回样例(用户名不存在): {'list': [{'error': 1}, {'error': 1},

    {'error': 1}, {'error': 1}, {'error': 1}, {'error': 1}, {'error': 1},

    {'error': 1}, {'error': 1}, {'error': 1}, {'error': 1}, {'error': 1}]}
    """
    response = {}
    res_list = []
    data = json.loads(request.body)
    name = data['name']
    year = datetime.now().year
    for index in range(12):
        month = index + 1
        nextmonth = (month+1)
        if month == 12:
            res_list.append(
                get_seller_rate(
                    name, date(year, month, 1).strftime("%Y-%m-%d"),
                    date(year+1, 1, 1).strftime("%Y-%m-%d")))
        else:
            res_list.append(
                get_seller_rate(
                    name, date(year, month, 1).strftime("%Y-%m-%d"),
                    date(year, nextmonth, 1).strftime("%Y-%m-%d")))
    for temp_list in res_list:
        if 'date' in temp_list:
            del temp_list['date']
    response['list'] = res_list
    return JsonResponse(response)


@login_required
@require_http_methods(['POST'])
def years_seller_grades(request):
    """
    本api用于获得两年内销售人员业绩可视化数据来源

    :url: data/years_seller_grades

    :前端传送数据: {'name': 'name'(为空时代表全体地推人员)}

    :返回: error状态码和业绩信息

    :返回值: Json字典

    :返回样例(用户名不存在): {'last_list': [{'sellcount': 1, 'sellmoney': 29.9,

    'signcount': 1, 'signmoney': 2999.9, 'error': 0, 'auditioncount': 1,

    'audition_rate': 100.0, 'sign_rate': 100.0}],

    'this_list': [{'sellcount': 1, 'sellmoney': 29.9, 'signcount': 1,

    'signmoney': 2999.9, 'error': 0, 'auditioncount': 1,

    'audition_rate': 100.0, 'sign_rate': 100.0}]}

    :返回样例(用户名不存在): {'last_list': [{'error': 1}],

    'this_list': [{'error': 1}]}
    """
    response = {}
    last_list = []
    this_list = []
    data = json.loads(request.body)
    name = data['name']
    year = datetime.now().year
    lastyear = year - 1
    nextyear = year + 1
    lastyear = date(lastyear, 1, 1)
    year = date(year, 1, 1)
    nextyear = date(nextyear, 1, 1)
    last_list.append(get_seller_rate(
        name, lastyear.strftime("%Y-%m-%d"),
        year.strftime("%Y-%m-%d")))
    this_list.append(get_seller_rate(
        name, year.strftime("%Y-%m-%d"),
        nextyear.strftime("%Y-%m-%d")))
    if 'date' in last_list[0]:
        del last_list[0]['date']
    if 'date' in this_list[0]:
        del this_list[0]['date']
    response['last_list'] = last_list
    response['this_list'] = this_list
    return JsonResponse(response)


def get_indate_allcc_grades(start, end):
    """
    本函数用于获得课程顾问相应时间内总销售信息

    :接收参数: start, end(string)%Y-%m-%d格式的日期字符串

    :返回: 全部课程顾问相应时间内对应的注册试听人数、收入和报名人数和收入

    :返回值: 字典
    """
    response = {}
    response['error'] = STATUS_CODE['Success']
    customers = Customer.objects.filter(date_cc__range=[start, end])
    customers = customers.exclude(cc=None)
    response['flow_num'] = customers.count()
    audition_num = 0
    audition_income = 0.0
    for customer in customers:
        if customer.audition_record.filter().count() != 0:
            audition_num += 1
            sellrecord = SellRecord.objects.get(customer=customer)
            sellerinfo = sellrecord.seller
            audition_income += sellerinfo.price
    response['audition_num'] = audition_num
    response['audition_income'] = round(audition_income, 2)
    ccrecords = CcRecord.objects.filter(date__range=[start, end], is_paid=True)
    response['signup_num'] = ccrecords.count()
    response['signup_income'] = round(get_records_money(ccrecords), 2)
    return response


def get_indate_cc_grade(name, start, end):
    """
    本函数用来根据名字和时间返回课程顾问的业绩

    :接收参数:  name(string)地推人员姓名，为空的时候代表全体

    start, end(string)%Y-%m-%d格式的日期字符串

    :返回: error状态码和课程顾问相应时间内对应的注册试听人数、收入和报名人数和收入

    :返回值: 字典
    """
    response = {}
    consults = User.objects.filter(
        username=name, user_type=USER_TYPE['consultant'])
    if consults.count() == 0:
        response['error'] = STATUS_CODE['User Not Found']
        return response
    response['error'] = STATUS_CODE['Success']
    consults = consults[0]
    customers = Customer.objects.filter(
        date_cc__range=[start, end], cc=consults)
    response['flow_num'] = customers.count()
    audition_num = 0
    audition_income = 0.0
    for customer in customers:
        if customer.audition_record.filter().count() != 0:
            audition_num += 1
            sellrecord = SellRecord.objects.get(customer=customer)
            sellerinfo = sellrecord.seller
            audition_income += sellerinfo.price
    response['audition_num'] = audition_num
    response['audition_income'] = round(audition_income, 2)
    ccrecords = CcRecord.objects.filter(
        date__range=[start, end], is_paid=True, cc=consults)
    response['signup_num'] = ccrecords.count()
    response['signup_income'] = round(get_records_money(ccrecords), 2)
    return response


def get_indate_cc_grades(name, start, end):
    """
    本函数用于补充课程顾问相应时间内销售信息及转化率

    :传入参数: name(string)地推人员姓名，为空的时候代表全体

    start, end(string)%Y-%m-%d格式的日期字符串

    :返回: 地推人员相应时间业绩以及试听率和报名率

    :返回值: 字典
    """
    response = {}
    date_cc_end = datetime.strptime(end, "%Y-%m-%d") - timedelta(hours=24)
    date_cc_end = date_cc_end.strftime("%Y-%m-%d")
    if name == '':
        response = get_indate_allcc_grades(start, date_cc_end)
    else:
        response = get_indate_cc_grade(name, start, date_cc_end)
        if response['error'] == STATUS_CODE['User Not Found']:
            return response
    if response['flow_num'] == 0:
        response['audition_rate'] = 0
    else:
        response['audition_rate'] = round(
            response['audition_num']/response['flow_num'], 2)*100
    if response['audition_num'] == 0:
        response['signup_rate'] = 0
    else:
        response['signup_rate'] = round(
            response['signup_num']/response['audition_num'], 2)*100
    response['date'] = start
    return response


@login_required
@require_http_methods(['POST'])
def today_cc_grades(request):
    """
    本api用于获取课程顾问当天对应注册试听人数、收入，报名人数、收入以及试听率和转化率

    :url: data/today_cc_grades

    :前端传入数据: data = {'name': 'cc'(为空时代表全部课程顾问)}

    :返回: 试听人数、注册试听收入、报名人数、报名收入、 试听率、 转化率

    :返回值: Json字典

    :返回样例(课程顾问存在): {'error': 0, 'flow_num': 1, 'audition_num': 1,

    'audition_income': 29.9, 'signup_num': 0, 'signup_income': 0.0,

    'audition_rate': 100.0, 'signup_rate': 0.0, 'date': '2018-08-29'}

    :返回样例(课程顾问不存在):{'error': 902}
    """
    response = {}
    data = json.loads(request.body)
    name = data['name']
    today = datetime.now()
    tomorrow = today + timedelta(hours=23, minutes=59, seconds=59)
    today = today.strftime("%Y-%m-%d")
    tomorrow = tomorrow.strftime("%Y-%m-%d")
    response = get_indate_cc_grades(name, today, tomorrow)
    return JsonResponse(response)


@login_required
@require_http_methods(['POST'])
def week_cc_grades(request):
    """
    本api用于获取课程顾问近7天对应注册试听人数、收入，报名人数、收入以及试听率和转化率

    :url: data/week_cc_grades

    :前端传入数据: data = {'name': 'cc'(为空时代表全部课程顾问)}

    :返回: 试听人数、注册试听收入、报名人数、报名收入、 试听率、 报名率

    :返回值: Json字典

    :返回样例(只显示了一天样例): {'list':

    [{'error': 0, 'flow_num': 1, 'audition_num': 1, 'audition_income': 29.9,

    'signup_num': 0, 'signup_income': 0.0, 'audition_rate': 100.0,

    'signup_rate': 0.0, 'date': '2018-08-23'} ··· ··· ]}

    :返回样例(用户名不存在): {'list': [{'error': 902}, {'error': 902},

    {'error': 902}, {'error': 902}, {'error': 902}, {'error': 902},

    {'error': 902}]}
    """
    response = {}
    res_list = []
    data = json.loads(request.body)
    name = data['name']
    today = datetime.now()
    start = today - timedelta(hours=24*6)
    for _ in range(7):
        end = start + timedelta(hours=24)
        res_list.append(get_indate_cc_grades(name, start.strftime(
            "%Y-%m-%d"), end.strftime("%Y-%m-%d")))
        start = end
    response['list'] = res_list
    return JsonResponse(response)


@login_required
@require_http_methods(['POST'])
def months_cc_grades(request):
    """
    本api用于获取课程顾问今年各月对应注册试听人数、收入

    报名人数、收入以及试听率和转化率

    :url: data/months_cc_grades

    :前端传入数据: data = {'name': 'cc'(为空时代表全部课程顾问)}

    :返回: 试听人数、注册试听收入、报名人数、报名收入、 试听率、 报名率

    :返回值: Json字典

    :返回样例(只显示了一个月样例): {'list':

    [{'error': 0, 'flow_num': 1, 'audition_num': 1, 'audition_income': 39.9,

    'signup_num': 0, 'signup_income': 0.0, 'audition_rate': 100.0,

    'signup_rate': 0.0} ··· ··· ]}

    :返回样例(用户名不存在): {'list': [{'error': 902} ··· ··· ]}
    """
    response = {}
    res_list = []
    data = json.loads(request.body)
    name = data['name']
    year = datetime.now().year
    for index in range(12):
        month = index + 1
        nextmonth = (month+1)
        if month == 12:
            res_list.append(
                get_indate_cc_grades(
                    name, date(year, month, 1).strftime("%Y-%m-%d"),
                    date(year+1, 1, 1).strftime("%Y-%m-%d")))
        else:
            res_list.append(
                get_indate_cc_grades(
                    name, date(year, month, 1).strftime("%Y-%m-%d"),
                    date(year, nextmonth, 1).strftime("%Y-%m-%d")))
    for temp_list in res_list:
        if 'date' in temp_list:
            del temp_list['date']
    response['list'] = res_list
    return JsonResponse(response)


@login_required
@require_http_methods(['POST'])
def years_cc_grades(request):
    """
    本api用于获取课程顾问近两年对应注册试听人数、收入

    报名人数、收入以及试听率和转化率

    :url: data/years_cc_grades

    :前端传入数据: data = {'name': 'cc'(为空时代表全部课程顾问)}

    :返回: 试听人数、注册试听收入、报名人数、报名收入、 试听率、 报名率

    :返回值: Json字典

    :返回样例(用户名存在): {'last_list':

    [{'error': 0, 'flow_num': 1, 'audition_num': 1, 'audition_income': 39.9,

    'signup_num': 1, 'signup_income': 4369.0, 'audition_rate': 100.0,

    'signup_rate': 100.0}], 'this_list': [{'error': 0, 'flow_num': 1,

    'audition_num': 1, 'audition_income': 39.9, 'signup_num': 1,

    'signup_income': 4369.0, 'audition_rate': 100.0, 'signup_rate': 100.0}]}

    :返回样例(用户名不存在): {'last_list': [{'error': 902}],

    'this_list': [{'error': 902}]}
    """
    response = {}
    last_list = []
    this_list = []
    data = json.loads(request.body)
    name = data['name']
    year = datetime.now().year
    lastyear = year - 1
    nextyear = year + 1
    lastyear = date(lastyear, 1, 1)
    year = date(year, 1, 1)
    nextyear = date(nextyear, 1, 1)
    last_list.append(get_indate_cc_grades(
        name, lastyear.strftime("%Y-%m-%d"),
        year.strftime("%Y-%m-%d")))
    this_list.append(get_indate_cc_grades(
        name, year.strftime("%Y-%m-%d"),
        nextyear.strftime("%Y-%m-%d")))
    if 'date' in last_list[0]:
        del last_list[0]['date']
    if 'date' in this_list[0]:
        del this_list[0]['date']
    response['last_list'] = last_list
    response['this_list'] = this_list
    return JsonResponse(response)


@login_required
@require_http_methods(['POST'])
def get_seller_distribution(request):
    """
    本api用于获取各城市的地推人数

    :url: data/get_seller_distribution

    :返回: 各个城市地推人数

    :返回值: Json字典

    :返回样例: {'list':

    [{'city': '北京', 'num': 1}, {'city': '上海', 'num': 3},

    {'city': '广州', 'num': 1}, {'city': '深圳', 'num': 1},

    {'city': '天津', 'num': 1}, {'city': '石家庄', 'num': 1}]}
    """
    response = {}
    citys = SellerInfo.objects.values('city').distinct()
    citys_num = []
    for city in citys:
        temp_dict = {}
        temp_dict['city'] = city['city']
        temp_dict['num'] = SellerInfo.objects.filter(city=city['city']).count()
        citys_num.append(temp_dict)
    response['list'] = citys_num
    return JsonResponse(response)


def get_audition_data_range(teacher_name, date_from, date_to):
    """
    本函数用于查看单个老师时间段内的试听业绩

    :传入数据: date_from 开始时间  date_to 截止时间 ；老师名字

    :返回数据: tuple (msg, list)

    """
    grade_list = {
        'name': teacher_name, 'audition_num': 0,
        'signup_num': 0, 'rate': 0}
    teachers = Teacher.objects.filter(name=teacher_name)
    if teachers.count() == 0:
        return (STATUS_CODE['User Not Found'], [])

    for teacher in teachers:
        for course in teacher.teacher.all():
            for section in course.sections.filter(
                    date__range=[date_from, date_to]):
                records = section.audition_record.all()
                grade_list['audition_num'] = (
                    records.count() + grade_list['audition_num'])
                grade_list['signup_num'] = (
                    records.filter(is_signedup=True).count()
                ) + grade_list['signup_num']
    grade_list['rate'] = (
        '0%' if grade_list['audition_num'] == 0 else
        format(grade_list['signup_num']/grade_list['audition_num'], '.0%'))
    return (STATUS_CODE['Success'], grade_list)


def get_date_start(date_to):
    """
    本函数用于返回本周，本月，本年度的起始时间

    :传入数据: date_to 截止时间

    :返回数据: dict{'year','month','week'}

    """
    from_week = (date_to - timedelta(days=date_to.isoweekday()))
    from_month = '%d-%02d-01' % (date_to.year, date_to.month)
    from_year = '%d-01-01' % (date_to.year)
    return {
        'year': from_year,
        'month': from_month,
        'week': from_week
    }


def get_audition_all_range(date_from, date_to):
    """
    本函数用于查看所有老师试听转化率数据

    :传入数据: date_from 开始时间 ; date_to 截止时间

    :返回数据: tuple (msg, list)

    """
    the_list = []
    for teacher in list(Teacher.objects.all().values('name')):
        result = get_audition_data_range(
            teacher['name'],
            date_from,
            date_to
        )[1]
        the_list.append(result)
    return the_list


@login_required
@require_http_methods(['POST'])
def audition_grades(request):
    """
    本api用于处理查看老师试听转化率的请求

    :前端发送数据: name: 老师姓名 ; date_from: 开始时间 ; date_to: 结束时间

    :url: data/audition_grades

    :返回类型: Json字典

    :返回内容1: key: 'msg'  value: 状态码 (0 或 705 或 902)

    :返回内容2: key: 'list' 单一数据

    :返回内容2: key: 'week' 'month' 'year'  本周 本月 本年度个人数据

                （老师姓名存在 而时间段数据为空时）

    :返回数据: value: name, audition_num, signup_num, rate

    """
    response = {}
    data = json.loads(request.body)
    if 'name' in data and 'date_from' in data and 'date_to' in data:
        today = datetime.now()
        start_dict = get_date_start(today)
        if data['name'] == "":
            if data['date_from'] is None or data['date_to'] is None:
                response['list'] = get_audition_all_range(
                    start_dict['month'], today
                )
            else:
                response['list'] = get_audition_all_range(
                    data['date_from'], data['date_to']
                )
        else:
            if data['date_from'] is None or data['date_to'] is None:
                response['week'] = get_audition_data_range(
                    data['name'], start_dict['week'], today)
                response['month'] = get_audition_data_range(
                    data['name'], start_dict['month'], today)
                response['year'] = get_audition_data_range(
                    data['name'], start_dict['year'], today)
            else:
                response['list'] = get_audition_data_range(
                    data['name'], data['date_from'], data['date_to']
                )
    else:
        response['msg'] = STATUS_CODE['Frontend Value Error']
    return JsonResponse(response)


@login_required
@require_http_methods(['POST'])
def superuser_import_courses(request):
    """
    本api用于处理超级管理员的请求

    :前端发送数据: FormData 包含文件

    :url: data/import_courses

    :返回类型: msg: 状态码 error 错误列表

    :返回格式: {'msg': 0, 'error': [{'msg': 910, 'name': '课程名'}]}

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
    result = import_courses(
        file_in,
        thefile.name,
    )
    response['msg'] = result[0]
    response['error'] = result[1]
    os.remove(path)
    return JsonResponse(response)


@login_required
@require_http_methods(['POST'])
def create_audition_records(request):
    """
    本api用于添加试听人数

    :url: data/create_audition_records

    :返回: error状态码

    :返回值: Json字典

    :返回样例: {'error': 0}

    :error状态码解释: 0(成功添加记录) 1(课节不存在) 902(用户不存在)
    """
    response = {}
    data = json.loads(request.body)
    customer_id = data['id']
    try:
        customer = Customer.objects.get(pk=customer_id)
    except Customer.DoesNotExist:
        response['error'] = STATUS_CODE['User Not Found']
        return JsonResponse(response)
    section_name = data['section_name']
    try:
        section = Section.objects.get(name=section_name)
    except Section.DoesNotExist:
        response['error'] = STATUS_CODE['Not Found']
        return JsonResponse(response)
    info = data['info']
    is_signedup = data['is_signedup']
    if is_signedup == '报名':
        customer.is_signedup = True
        AuditionRecord.objects.create(
            customer=customer, section=section,
            is_signedup=True, info=info)
    else:
        AuditionRecord.objects.create(
            customer=customer, section=section,
            is_signedup=False, info=info)
    customer.audition_count += 1
    customer.save()
    response['error'] = STATUS_CODE['Success']
    return JsonResponse(response)
