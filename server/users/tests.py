# -*- coding: utf-8 -*-

'''本文件用于测试'''
import json
import os

from django.test import Client, TestCase

from customers.models import Customer
from datas.models import OperationLogs
from server.settings import MEDIAFILES_DIRS
from statuscode import STATUS_CODE, USER_TYPE

from .models import SellerInfo, User

# Create your tests here.


class SellerviewsTestCase(TestCase):
    '''
    地推人员视图测试
    '''

    def setUp(self):
        '''
        初始化数据
        '''
        user = User.objects.create(
            username='seller', user_type=USER_TYPE['seller'])
        user.set_password('123')
        user.save()
        seller = SellerInfo(seller=user, price=22, city='cq')
        seller.save()
        user = User.objects.create(
            username='iseller', user_type=USER_TYPE['consultant'])
        user.set_password('321')
        user.save()

    def test_qrcode(self):
        '''
        测试二维码生成和获得返回功能
        '''
        client = Client()
        client.login(username='seller', password='123')
        user = User.objects.get(username='seller')
        infoid = SellerInfo.objects.get(seller=user).id
        path_delete = os.path.join(
            MEDIAFILES_DIRS[0] + '/img', str(infoid) + '.png')
        if os.path.exists(path_delete):
            os.remove(path_delete)
        path = ''.join(['/static/img/', str(infoid), '.png'])
        response = client.post(
            '/user/qrcode',
            content_type='application/json'
        )
        data = (json.loads(response.content))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['path'], path)
        self.assertEqual(data['msg'], STATUS_CODE['Success'])
        response2 = client.post(
            '/user/qrcode',
            content_type='application/json'
        )
        data2 = (json.loads(response2.content))
        self.assertEqual(data2['msg'], STATUS_CODE['Success'])
        os.remove(path_delete)

    def test_identity_error(self):
        '''
        测试生成二维码时输入人员的身份不正确时返回Identity Error code
        '''
        client = Client()
        client.login(username='iseller', password='321')
        response = client.post(
            '/user/qrcode',
            content_type='application/json'
        )
        data = (json.loads(response.content))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['msg'], STATUS_CODE['Identity Error'])


class SuperuserViewLogTestCase(TestCase):
    '''本类用于测试超级管理员查看日志'''

    def setUp(self):
        user = User.objects.create(
            username='superuser', user_type=USER_TYPE['superuser'])
        user.set_password('superuser')
        user.save()
        OperationLogs.objects.create(
            operator=user, type=1, username='person1',
            info=user.username+"删除了员工person1")

    def test_view_log(self):
        '''测试日期内有日志的情况'''
        client = Client()
        client.login(username='superuser', password='superuser')
        data = {
            'start': '2018-06-06',
            'end': '2018-09-11'
        }
        response = client.post(
            '/user/superuser_viewlog', data,
            content_type='application/json'
        )
        content = json.loads(response.content)
        self.assertEqual(content['error'], STATUS_CODE['Success'])

    def test_view_nolog(self):
        '''测试日期内没有日志的情况'''
        client = Client()
        client.login(username='superuser', password='superuser')
        data = {
            'start': '2018-06-06',
            'end': '2018-07-11'
        }
        response = client.post(
            '/user/superuser_viewlog', data,
            content_type='application/json'
        )
        content = json.loads(response.content)
        self.assertEqual(content['error'], STATUS_CODE['Not Found'])


class SuperuserArrCCTestCase(TestCase):
    """
    本类用于测试超级管理员给学员安排课程顾问
    """

    def setUp(self):
        user = User.objects.create(
            username='superuser', user_type=USER_TYPE['superuser'])
        user.set_password('superuser')
        user.save()
        cc = []
        for i in range(3):
            temp_cc = User.objects.create(
                username='cc'+str(i), user_type=USER_TYPE['consultant'])
            cc.append(temp_cc)
        user_cus1 = User.objects.create(username='13812349874')
        User.objects.create(username='13812347777')
        Customer.objects.create(
            user=user_cus1, child_name='child1')
        Customer.objects.create(
            user=user_cus1, child_name='child2', cc=cc[0])

    def test_get_without_cc(self):
        """
        测试返回学生信息
        """
        client = Client()
        client.login(username='superuser', password='superuser')
        response = client.post('/user/superuser_view_newstu',
                               content_type='application/json')
        content = json.loads(response.content)
        self.assertEqual(content['error'], STATUS_CODE['Success'])

    def test_get_ccinfo(self):
        """
        测试返回课程顾问信息
        """
        client = Client()
        client.login(username='superuser', password='superuser')
        response = client.post('/user/superuser_get_cc',
                               content_type='application/json')
        content = json.loads(response.content)
        self.assertEqual(content['error'], STATUS_CODE['Success'])

    def test_arr_cc(self):
        """
        测试分配课程顾问
        """
        client = Client()
        client.login(username='superuser', password='superuser')
        customer_id = Customer.objects.get(child_name='child1').id
        cc_id = User.objects.get(username='cc1').id
        User.objects.get(pk=cc_id)
        data = {
            'customer_id': customer_id,
            'cc_id': cc_id
        }
        response = client.post('/user/superuser_arrange_cc', data,
                               content_type='application/json')
        content = json.loads(response.content)
        customer = Customer.objects.get(child_name='child1')
        self.assertEqual(content['error'], STATUS_CODE['Success'])
        self.assertFalse(customer.cc is None)
