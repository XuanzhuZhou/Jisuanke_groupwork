# -*- coding: utf-8 -*-

'''本文件用于测试'''
import json
from datetime import datetime, timedelta

from django.test import Client, TestCase

from statuscode import DATE_CODE, STATUS_CODE, USER_TYPE
from users.models import User

from .models import Courses, Teacher, Section
from .views import init_sections


class EduAdminCourseInfoTestCase(TestCase):
    '''本类用于测试教务老师更改课程和课节信息'''

    def setUp(self):
        eduadmin = User.objects.create(
            username='eduadmin', user_type=USER_TYPE['eduadmin']
        )
        eduadmin.set_password('eduadmin')
        eduadmin.save()
        teacher = Teacher.objects.create(name='teacher', tel='15803331570')
        for i in range(3):
            Teacher.objects.create(
                name='testteacher'+str(i), tel='1580333157'+str(i+1))
        course = Courses.objects.create(
            name='course', teacher_id=teacher, time='8:00',
            date=DATE_CODE['Saturday'], total_sec=48, price=2468
        )
        start = datetime.strptime('2018-7-4', "%Y-%m-%d")
        for i in range(3):
            Section.objects.create(
                course_id=course, count=i+1,
                name=course.name+'<'+str(i+1)+'>',
                date=start+timedelta(hours=24*7*i),
                start_time='8:00',
                end_time='10:00',
                location='classIn102')
        Section.objects.create(
            course_id=course, count=i+1,
            name=course.name+'<'+str(i+1)+'>',
            date='2018-08-30',
            start_time='8:00',
            end_time='10:00',
            location='classIn102')
        Section.objects.create(
            course_id=course, count=12, name='testsection',
            date='2018-09-12',
            start_time='8:00',
            end_time='10:00',
            location='classIn102')

    def test_view_courseinfo(self):
        '''测试查看课程细则'''
        client = Client()
        course_id = Courses.objects.get(name='course').id
        data = {
            'id': course_id
        }
        client.login(username='eduadmin', password='eduadmin')
        response = client.post(
            '/course/edu_courses_info', data, content_type='application/json')
        content = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('course_info' in content)
        self.assertTrue('teacher_info' in content)
        self.assertTrue('section_info' in content)

    def test_change_courseinfo(self):
        '''测试更改课程信息'''
        client = Client()
        course_id = Courses.objects.get(name='course').id
        data = {
            'id': course_id,
            'teacher_name': 'teacher',
            'name': 'newcoursename',
            'time': '18:00:00',
            'time_length': 120,
            'price': 2489
        }
        client.login(username='eduadmin', password='eduadmin')
        response = client.post(
            '/course/change_course_info', data,
            content_type='application/json')
        course = Courses.objects.get(pk=course_id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(course.name, 'newcoursename')
        self.assertEqual(str(course.time), '18:00:00')

    def test_change_sectioninfo(self):
        '''测试更改课节信息'''
        client = Client()
        section = Section.objects.get(name='testsection')
        data = {
            'section_id': section.pk,
            'count': 13,
            'section_name': 'newsectionname',
            'date': '2019-10-20',
            'start_time': '14:00:00',
            'end_time': '16:00:00',
            'location': 'classIn501'
        }
        client.login(username='eduadmin', password='eduadmin')
        response = client.post(
            '/course/change_section_info', data,
            content_type='application/json')
        section = Section.objects.get(name='newsectionname')
        content = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(content['error'], STATUS_CODE['Success'])
        self.assertEqual(section.count, 13)
        self.assertEqual(section.location, 'classIn501')


class InitSectionTestCase(TestCase):
    '''本类用于测试初始化课节信息'''

    def test_init_section(self):
        '''本函数用来测试初始化课节函数'''
        teacher = Teacher.objects.create(name='teacher', tel='15803331570')
        course = Courses.objects.create(
            name='course', teacher_id=teacher,
            date=DATE_CODE['Saturday'], total_sec=48, price=2468)
        course.time = datetime.strptime('8:00:00', '%H:%M:%S').time()
        course.save()
        init_sections(course,
                      datetime.strptime('2018-07-10', "%Y-%m-%d").date())
        self.assertTrue(Section.objects.filter(course_id=course).count(), 48)


class AddtheCourseTestCase(TestCase):
    '''本类用于测试手动添加课程'''

    def setUp(self):
        eduadmin = User.objects.create(
            username='eduadmin', user_type=USER_TYPE['eduadmin']
        )
        eduadmin.set_password('eduadmin')
        eduadmin.save()
        Teacher.objects.create(name='teacher', tel='15803331570')

    def test_add_course(self):
        '''测试输入正确的老师姓名的情况'''
        client = Client()
        data = {
            'teacher_name': 'teacher',
            'name': 'newcourse',
            'time': '16:00:00',
            'date': 6,
            'time_length': 120,
            'total_sec': 48,
            'price': 2468,
            'start_date': '2018-08-29'
        }
        client.login(username='eduadmin', password='eduadmin')
        response = client.post(
            '/course/add_new_course', data,
            content_type='application/json')
        course = Courses.objects.get(name='newcourse')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(course.date, 6)

    def test_unadd_course(self):
        '''测试输入不存在的老师姓名的情况'''
        client = Client()
        data = {
            'teacher_name': 'noteacher',
            'name': 'newcourse',
            'time': '16:00:00',
            'date': 6,
            'time_length': 120,
            'total_sec': 48,
            'price': 2468,
            'start_date': '2018-08-29'
        }
        client.login(username='eduadmin', password='eduadmin')
        response = client.post(
            '/course/add_new_course', data,
            content_type='application/json')
        content = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(content['error'], STATUS_CODE['Not Found'])


class AddSectionTestCase(TestCase):
    '''本类用于测试增加课节'''

    def setUp(self):
        eduadmin = User.objects.create(
            username='eduadmin', user_type=USER_TYPE['eduadmin']
        )
        eduadmin.set_password('eduadmin')
        eduadmin.save()
        teacher = Teacher.objects.create(name='teacher', tel='15803331570')
        Courses.objects.create(
            name='course', teacher_id=teacher, time='8:00',
            date=DATE_CODE['Saturday'], total_sec=48, price=2468
        )

    def test_add_section(self):
        '''本函数用来测试增加课节'''
        client = Client()
        course = Courses.objects.get(name='course')
        data = {
            'id': course.id,
            'count': 49,
            'section_name': 'addsectionname',
            'date': '2019-10-20',
            'start_time': '14:00:00',
            'end_time': '16:00:00',
            'location': 'classIn501'
        }
        client.login(username='eduadmin', password='eduadmin')
        response = client.post(
            '/course/add_section', data,
            content_type='application/json')
        content = json.loads(response.content)
        section = Section.objects.get(name='addsectionname')
        course = Courses.objects.get(name='course')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(content['error'], STATUS_CODE['Success'])
        self.assertTrue(course.total_sec == 49)
        self.assertEqual(section.count, 49)
