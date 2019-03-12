# -*- coding: utf-8 -*-

'''本文件用于测试customers views'''
import json

from django.test import Client, TestCase

from courses.models import Courses, Section, Teacher
from datas.models import CcRecord
from statuscode import STATUS_CODE, USER_TYPE
from users.models import User
from api.models import VerifyCode

from .views import Customer

# Create your tests here.


class CustomerViewTestCase(TestCase):
    '''家长api测试'''

    def setUp(self):
        '''初始化数据'''
        teacher = Teacher.objects.create(name='teacher1', tel='test_tel_1')
        course1 = Courses.objects.create(
            name='course1', teacher_id=teacher, total_sec=30)
        course2 = Courses.objects.create(
            name='course2', teacher_id=teacher, total_sec=30)
        user1 = User.objects.create(
            username='customer', user_type=USER_TYPE['customer'])
        user1.set_password('123')
        user1.save()
        user2 = User.objects.create(
            username='other', user_type=USER_TYPE['superuser'])
        user2.set_password('321')
        user2.save()
        cc = User.objects.create(
            username='consultant', user_type=USER_TYPE['consultant'])
        cc.save()
        customer1 = Customer.objects.create(
            user=user1, child_name='child1', cc=cc, is_paid=True)
        customer1.takes.set([course1, course2])
        customer2 = Customer.objects.create(
            user=user1, child_name='child2', cc=cc)
        customer1.save()
        customer2.save()
        CcRecord.objects.create(
            customer=customer1,
            cc=cc, info='test', money=30,
            trade_no='1', is_paid=False
        )
        CcRecord.objects.create(
            customer=customer2,
            cc=cc, info='test_next',
            money=40, is_paid=True
        )
        VerifyCode.objects.create(code='1234', tel='customer')
        VerifyCode.objects.create(code='1234', tel='other')
        VerifyCode.objects.create(code='0987', tel='other')
        VerifyCode.objects.create(code='2234', tel='customer')

    def test_get_course(self):
        '''本函数用来测试家长获得课程数据api'''
        client = Client()
        client.login(username="customer", password="123")
        response = client.post(
            '/customer/courses',
            content_type='application/json'
        )
        data = (json.loads(response.content))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data['list']), 3)

    def test_pay_record_success(self):
        '''本函数用来测试家长查看待付款信息成功时'''
        client = Client()
        client.login(username='customer', password='123')
        response = client.post(
            '/customer/pay_records',
            content_type='application/json'
        )
        data = (json.loads(response.content))
        self.assertEqual(data['msg'], STATUS_CODE['Success'])

    def test_identity_error(self):
        '''本函数用来测试身份错误的情况'''
        client = Client()
        client.login(username='other', password='321')
        urls_list = ['refund', 'courses', 'info',
                     'sections', 'refund_cancel']
        for url in urls_list:
            response = client.post(
                '/customer/' + url,
                content_type='application/json'
            )
            data = (json.loads(response.content))
            self.assertEqual(response.status_code, 200)
            self.assertEqual(data['msg'], STATUS_CODE['Identity Error'])

    def test_info_view(self):
        '''本函数用来测试家长查看孩子信息请求api'''
        client = Client()
        client.login(username='customer', password='123')
        response = client.post(
            '/customer/info',
            content_type='application/json'
        )
        data = (json.loads(response.content))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data['list']), 2)

    def test_refund_success(self):
        '''本函数用来测试家长退款请求函数信息正确时'''
        client = Client()
        client.login(username='customer', password='123')
        course_id = Courses.objects.get(name='course1').id
        response = client.post(
            '/customer/refund',
            {
                'course_id': course_id,
                'child_name': 'child1',
                'info': 'testinfo'
            },
            content_type='application/json'
        )
        data = (json.loads(response.content))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['msg'], STATUS_CODE['Success'])

    def test_refund_fail(self):
        '''本函数用来测试家长退款请求函数信息错误时'''
        client = Client()
        client.login(username='customer', password='123')
        course_id = len(Courses.objects.all())+1
        response = client.post(
            '/customer/refund',
            {
                'course_id': course_id,
                'child_name': 'child1',
                'info': 'testinfo'
            },
            content_type='application/json'
        )
        data = (json.loads(response.content))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['msg'], STATUS_CODE['Course Not Found'])

    def test_refund_cancel(self):
        '''本函数用来测试家长取消退款成功时'''
        client = Client()
        client.login(username='customer', password='123')
        course_id = Courses.objects.get(name='course1').id
        response = client.post(
            '/customer/refund_cancel',
            {
                'course_id': course_id,
                'child_name': 'child1',
            },
            content_type='application/json'
        )
        data = (json.loads(response.content))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['msg'], STATUS_CODE['Success'])

    def test_register_exists(self):
        '''本函数用来测试家长注册孩子已存在时'''
        client = Client()
        response = client.post(
            '/customer/register',
            {
                'username': 'customer',
                'child_name': 'child1',
                'code': '1234',
            },
            content_type='application/json'
        )
        data = (json.loads(response.content))
        self.assertEqual(data['msg'], STATUS_CODE['Customer Already Exists'])

    def test_register_not_found(self):
        '''本函数用来测试注册时家长验证码错误'''
        client = Client()
        response = client.post(
            '/customer/register',
            {
                'username': 'customer',
                'child_name': 'child1',
                'code': '2344'
            },
            content_type='application/json'
        )
        data = (json.loads(response.content))
        self.assertEqual(data['msg'], STATUS_CODE['Verify Code Error'])

    def test_register_miss_value(self):
        '''本函数用来测试注册时缺少请求参数'''
        client = Client()
        response = client.post(
            '/customer/register',
            {
                'username': 'customer',
            },
            content_type='application/json'
        )
        data = (json.loads(response.content))
        self.assertEqual(data['msg'], STATUS_CODE['Verify Code Error'])

    def test_register_need_pay(self):
        '''本函数用来测试家长注册待付款'''
        client = Client()
        response = client.post(
            '/customer/register',
            {
                'username': 'customer',
                'child_name': 'child2',
                'code': '1234',
            },
            content_type='application/json'
        )
        data = (json.loads(response.content))
        self.assertEqual(data['msg'], STATUS_CODE['Success'])

    def test_view_section(self):
        '''本函数用来测试家长查看课节功能'''
        client = Client()
        client.login(username='customer', password='123')
        course = Courses.objects.get(name='course1')
        for i in range(5):
            Section.objects.create(
                course_id=course,
                count=i+1,
                date="2000-02-02",
                start_time="00:00:01",
                end_time="00:00:02",
                location="location").save()
        response = client.post(
            '/customer/sections',
            {
                'course_id': course.id,
            },
            content_type='application/json'
        )
        data = (json.loads(response.content))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['msg'], STATUS_CODE['Success'])

    def test_login_code_success(self):
        '''本函数用来测试家长用验证码登录成功时'''
        client = Client()
        response = client.post(
            '/customer/login_code',
            {
                'username': 'customer',
                'code': '1234',
            },
            content_type='application/json'
        )
        data = (json.loads(response.content))
        self.assertEqual(data['msg'], STATUS_CODE['Success'])

    def test_login_code_error(self):
        '''本函数用来测试家长用验证码登录验证码错误时'''
        client = Client()
        response = client.post(
            '/customer/login_code',
            {
                'username': 'customer',
                'code': '4321',
            },
            content_type='application/json'
        )
        data = (json.loads(response.content))
        self.assertEqual(data['msg'], STATUS_CODE['Verify Code Error'])

    def test_login_code_invalid(self):
        '''本函数用来测试家长用验证码登录却未注册时'''
        client = Client()
        response = client.post(
            '/customer/login_code',
            {
                'username': 'invalid',
                'code': '1234',
            },
            content_type='application/json'
        )
        data = (json.loads(response.content))
        self.assertEqual(data['msg'], STATUS_CODE['User Not Found'])

    def test_register_success_error(self):
        '''本函数用来测试注册成功后错误前端请求'''
        client = Client()
        response = client.post(
            '/customer/register_success',
            {
                'username': 'customer',
            },
            content_type='application/json'
        )
        data = (json.loads(response.content))
        self.assertEqual(data['msg'], STATUS_CODE['Frontend Value Error'])

    def test_register_success(self):
        '''本函数用来测试注册付款成功后请求'''
        client = Client()
        response = client.post(
            '/customer/register_success',
            {
                'username': 'customer',
                'child_name': 'child2',
            },
            content_type='application/json'
        )
        data = (json.loads(response.content))
        self.assertEqual(data['msg'], STATUS_CODE['Success'])


class CustomerIdentityTest(TestCase):
    '''本函数用测试家长非验证码登录的api'''

    def setUp(self):
        '''本函数用来初始化'''
        user1 = User.objects.create(
            username='customer', user_type=USER_TYPE['customer'])
        user1.set_password('123')
        user1.save()

    def test_login_value_empty(self):
        '''本函数用来测试家长用验证码登录数据为空时'''
        client = Client()
        response = client.post(
            '/customer/login_code',
            content_type='application/json'
        )
        response2 = client.post(
            '/customer/login_password',
            content_type='application/json'
        )
        data = (json.loads(response.content))
        self.assertEqual(data['msg'], STATUS_CODE['Frontend Value Error'])
        data2 = (json.loads(response2.content))
        self.assertEqual(data2['msg'], STATUS_CODE['Frontend Value Error'])

    def test_login_password_success(self):
        '''本函数用来测试家长用密码登录成功时'''
        client = Client()
        response = client.post(
            '/customer/login_password',
            {
                'username': 'customer',
                'password': '123',
            },
            content_type='application/json'
        )
        data = (json.loads(response.content))
        self.assertEqual(data['msg'], STATUS_CODE['Success'])

    def test_login_password_error(self):
        '''本函数用来测试家长用密码登录验证码错误时'''
        client = Client()
        response = client.post(
            '/customer/login_password',
            {
                'username': 'customer',
                'password': '4321',
            },
            content_type='application/json'
        )
        data = (json.loads(response.content))
        self.assertEqual(data['msg'], STATUS_CODE['Password Not Match'])

    def test_login_password_invalid(self):
        '''本函数用来测试家长用密码登录却未注册时'''
        client = Client()
        response = client.post(
            '/customer/login_password',
            {
                'username': 'invalid',
                'password': '1234',
            },
            content_type='application/json'
        )
        data = (json.loads(response.content))
        self.assertEqual(data['msg'], STATUS_CODE['User Not Found'])
