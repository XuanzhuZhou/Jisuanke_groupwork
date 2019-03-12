# -*- coding:  utf-8 -*-
'''本文件用于实现教务老师更改课程及课节信息的api接口'''
import json
from datetime import date, datetime, timedelta

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from statuscode import STATUS_CODE

from .models import Courses, Section, Teacher


def get_teacher_info():
    """
    本函数用于获取所有老师信息

    :返回: error标识和老师信息

    :返回值: 字典

    :返回样例(老师信息存在): {'error': 0, 'list': [{'id': 1, 'name': 'teacher',

    'tel': '15803331570'}, {'id': 2, 'name': 'testteacher0',

    'tel': '15803331571'}, {'id': 3, 'name': 'testteacher1',

    'tel': '15803331572'}, {'id': 4, 'name': 'testteacher2',

    'tel': '15803331573'}]}}

    :返回样例(老师信息不存在): {'error': 1}
    """
    results = {}
    teachers = Teacher.objects.filter()
    if teachers.count == 0:
        results['error'] = STATUS_CODE['Not Found']
        results['list'] = []
        return results
    results['error'] = STATUS_CODE['Success']
    results['list'] = list(teachers.values())
    return results


def get_unsection_info(course):
    """
    本函数用于获取某门课程未销课的课节信息

    :返回: error标识和老师信息

    :接收参数: Courses实例对象

    :返回值: 字典

    :返回样例(课节信息存在): {'error': 0, 'list': [{'id': 1, 'course_id_id': 1,
    'count': 1, 'name': 'course<1>', 'date': '2018-07-04',

    'start_time': '08:00:00', 'end_time': '10:00:00', 'location': 'classIn102',

    'is_cancel': False}, {'id': 2, 'course_id_id': 1, 'count': 2, 'name':

    'course<2>', 'date': '2018-07-11', 'start_time': '08:00:00', 'end_time':

    '10:00:00', 'location': 'classIn102', 'is_cancel': False}, {'id': 3,

    'course_id_id': 1, 'count': 3, 'name': 'course<3>', 'date': '2018-07-18',

    'start_time': '08:00:00', 'end_time': '10:00:00', 'location': 'classIn102',

    'is_cancel': False}]}

    :返回样例(课节信息不存在): {'error': 1, 'list': []}
    """
    results = {}
    sections = course.sections.filter(is_cancel=False)
    if sections.count() == 0:
        results['error'] = STATUS_CODE['Not Found']
        results['list'] = []
        return results
    results['error'] = STATUS_CODE['Success']
    results['list'] = list(sections.values())
    return results


@login_required
@require_http_methods(['POST'])
def edu_courses_info(request):
    """
    本api用于查看课程课节及老师细则，方便更改课程信息

    :url: course/edu_courses_info

    :前端传入数据: {'id': int}

    :返回: 课程信息、老师信息、对应课节信息

    :返回值: Json字典

    :返回样例: {'course_info': {'name': 'course', 'teacher': 'teacher',

    'time': '08:00:00', 'time_length': 120, 'price': 2468.0},

    'teacher_info': {'error': 0, 'list':

    [{'id': 1, 'name': 'teacher', 'tel': '15803331570'},

    {'id': 2, 'name': 'testteacher0', 'tel': '15803331571'}]},

    'section_info': {'error': 0, 'list':

    [{'id': 1, 'course_id_id': 1, 'count': 1, 'name': 'course<1>',

    'date': '2018-07-04', 'start_time': '08:00:00', 'end_time': '10:00:00',

    'location': 'classIn102', 'is_cancel': False},

    {'id': 2, 'course_id_id': 1, 'count': 2, 'name': 'course<2>',

    'date': '2018-07-11', 'start_time': '08:00:00', 'end_time': '10:00:00',

    'location': 'classIn102', 'is_cancel': False}]}}
    """
    response = {}
    data = json.loads(request.body)
    course_id = data['id']
    course = Courses.objects.get(pk=course_id)
    course_info = {}
    course_info['name'] = course.name
    course_info['teacher'] = course.teacher_id.name
    course_info['time'] = course.time
    course_info['time_length'] = course.time_length
    course_info['price'] = round(course.price, 2)
    response['course_info'] = course_info
    teacher_info = get_teacher_info()
    response['teacher_info'] = teacher_info
    section_info = get_unsection_info(course)
    response['section_info'] = section_info
    return JsonResponse(response)


@login_required
@require_http_methods(['POST'])
def change_course_info(request):
    """
    本api用于更改课程信息

    :url: course/change_course_info

    :前端传入数据(全部必填): id(课程id) teacher_name(老师名字) time(课程开始时间)

    time_length(课程时长) price(课程价格)

    :返回: error状态码

    :返回值: Json字典

    :返回样例: {'error': 0}或{'error': 1}

    :状态码解释: 0 操作成功 1 老师不存在
    """
    response = {}
    data = json.loads(request.body)
    if Teacher.objects.filter(name=data['teacher_name']).count() == 0:
        response['error'] = STATUS_CODE['Not Found']
        return JsonResponse(response)
    teacher = Teacher.objects.get(name=data['teacher_name'])
    course = Courses.objects.get(pk=data['id'])
    course.name = data['name']
    course.teacher_id = teacher
    course.price = data['price']
    course.time_length = data['time_length']
    time = datetime.strptime(data['time'], '%H:%M:%S').time()
    if course.time != time:
        sections = course.sections.filter(
            is_cancel=False, date__gte=date.today())
        for section in sections:
            section.start_time = time
            section.end_time = (
                datetime.combine(date(1, 1, 1), time) +
                timedelta(minutes=data['time_length'])).time()
            section.save()
    course.time = time
    course.save()
    response['error'] = STATUS_CODE['Success']
    return JsonResponse(response)


@login_required
@require_http_methods(['POST'])
def add_new_course(request):
    """
    本api用于教务手动添加新课程

    :url: course/add_new_course

    :前端传入数据样例: data = {'teacher_name': 'teachername',

    'name': 'coursename', 'time': '16:00:00','date': 6, 'time_length': 120,

    'total_sec': 48, 'price': 2468.9, 'start_date': '2018-08-29'}

    :返回: error状态码

    :返回值: Json字典

    :返回样例: {'error': 0}或{'error': 1}

    :状态码解释: 0 操作成功 1 老师不存在
    """
    response = {}
    data = json.loads(request.body)
    teacher_name = data['teacher_name']
    if Teacher.objects.filter(name=teacher_name).count() == 0:
        response['error'] = STATUS_CODE['Not Found']
        return JsonResponse(response)
    teacher = Teacher.objects.get(name=teacher_name)
    course = Courses.objects.create(
        name=data['name'], teacher_id=teacher,
        time=datetime.strptime(data['time'], '%H:%M:%S').time(),
        date=int(data['date']), time_length=int(data['time_length']),
        total_sec=int(data['total_sec']), price=float(data['price']))
    init_sections(
        course, datetime.strptime(data['start_date'], '%Y-%m-%d').date())
    response['error'] = STATUS_CODE['Success']
    return JsonResponse(response)


@login_required
@require_http_methods(['POST'])
def change_section_info(request):
    """
    本api用于更改未销课的课节信息

    :url: course/change_section_info

    :前端传入数据(全部必填): section_id(课节id) count(课节数) section_name(课节名)

    date(该课节上课日期) start_time(该课节开始时间) end_time(该课节结束时间)

    location(上课地点)

    :返回: error状态码

    :返回值: Json字典

    :返回样例: {'error': 0}

    :状态码解释: 0 操作成功
    """
    response = {}
    data = json.loads(request.body)
    section_id = data['section_id']
    date_temp = datetime.strptime(data['date'], '%Y-%m-%d').date()
    start_time = datetime.strptime(data['start_time'], '%H:%M:%S').time()
    end_time = datetime.strptime(data['end_time'], '%H:%M:%S').time()
    section = Section.objects.get(pk=section_id)
    section.count = data['count']
    section.name = data['section_name']
    section.date = date_temp
    section.start_time = start_time
    section.end_time = end_time
    section.location = data['location']
    section.save()
    response['error'] = STATUS_CODE['Success']
    return JsonResponse(response)


@login_required
@require_http_methods(['POST'])
def add_section(request):
    """
    本api用于添加课节

    :url: course/add_section

    :前端传入数据(全部必填): id(课程id) count(课节数) section_name(课节名)

    date(该课节上课日期) start_time(该课节开始时间) end_time(该课节结束时间)

    location(上课地点)

    :返回: error状态码

    :返回值: Json字典

    :返回样例: {'error': 0}或{'error': 1}

    :状态码解释: 0 操作成功 1 课程未找到
    """
    response = {}
    data = json.loads(request.body)
    course_id = data['id']
    if Courses.objects.filter(pk=course_id) == 0:
        response['error'] = STATUS_CODE['Not Found']
        return response
    date_temp = datetime.strptime(data['date'], '%Y-%m-%d').date()
    start_time = datetime.strptime(data['start_time'], '%H:%M:%S').time()
    end_time = datetime.strptime(data['end_time'], '%H:%M:%S').time()
    course = Courses.objects.get(pk=course_id)
    course.total_sec += 1
    course.save()
    Section.objects.create(
        course_id=course, count=data['count'], name=data['section_name'],
        date=date_temp, start_time=start_time, end_time=end_time,
        location=data['location'])
    response['error'] = STATUS_CODE['Success']
    return JsonResponse(response)


def init_sections(course, start_date):
    """
    本函数用于初始化课节信息

    :接收参数: Courses实例对象, start_date(课程开课日期%Y-%m-%s)
    """
    start_time = course.time
    end_time = (datetime.combine(date(1, 1, 1), start_time) +
                timedelta(minutes=course.time_length)).time()
    for i in range(course.total_sec):
        Section.objects.create(
            course_id=course, count=i+1,
            name=course.name+'<'+str(i+1)+'>',
            date=start_date+timedelta(hours=i*24*7),
            start_time=start_time, end_time=end_time,
            location='classIn'
        )
