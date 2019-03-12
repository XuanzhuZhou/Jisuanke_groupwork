# -*- coding: utf-8 -*-

'''本文件用于测试'''


import json
from datetime import datetime, timedelta

from django.test import Client, TestCase

from courses.models import Courses, Section, Teacher
from customers.models import Customer, search_customer
from datas.models import CcRecord, RefundRecord, SellRecord, get_course
from statuscode import STATUS_CODE, USER_TYPE
from users.models import SellerInfo, User

from .models import VerifyCode, check_mobile


class BackendloginoutTestCase(TestCase):
    '''本类用于测试后台人员登录和退出登录功能'''

    def setUp(self):
        user = User(username='cb', user_type=USER_TYPE['consultant'])
        user.set_password('cb')
        user.save()

    def test_login_error_0_password(self):
        '''登录密码错误的测试'''
        client = Client()
        data = {
            'type': '3',
            'user': 'cb',
            'password': 'cc'
        }
        rep = client.post('/api/login', data, content_type='application/json')
        content = json.loads(rep.content)
        self.assertEqual(rep.status_code, 200)
        self.assertTrue(content['error'] == STATUS_CODE['Password Not Match'])

    def test_login_error_0_username(self):
        '''登录用户名错误的测试'''
        client = Client()
        data = {
            'type': '3',
            'user': 'cc',
            'password': 'cb'
        }
        rep = client.post('/api/login', data, content_type='application/json')
        content = json.loads(rep.content)
        self.assertEqual(rep.status_code, 200)
        self.assertTrue(content['error'] == STATUS_CODE['User Not Found'])

    def test_login_error_1(self):
        '''登录身份信息错误的测试'''
        client = Client()
        data = {
            'type': '4',
            'user': 'cb',
            'password': 'cb'
        }
        rep = client.post('/api/login', data, content_type='application/json')
        content = json.loads(rep.content)
        self.assertEqual(rep.status_code, 200)
        self.assertTrue(content['error'] == STATUS_CODE['Identity Error'])

    def test_logout_success(self):
        '''已登录的情况下退出登录'''
        client = Client()
        client.login(username='cb', password='cb')
        rep = client.post('/api/logout')
        content = json.loads(rep.content)
        self.assertEqual(rep.status_code, 200)
        self.assertTrue(content['error'] == STATUS_CODE['Success'])


class VerifyCodeTestCase(TestCase):
    '''测试发送验证码的类'''

    client = Client()

    def setUp(self):
        member = VerifyCode('1234', '15123451234')
        member.save()
        member = VerifyCode('0987', '15223451234')
        member.save()
        member = VerifyCode('1234', '15323451234')
        member.save()

    # def test_send_code_success(self):
    #     '''测试正确发送验证码'''
    #     client = Client()
    #     msg = {"tel": "15804868839",
    #            "dmac": "ff:ff:ff:ff:ff:ff"}
    #     rep = client.post("/api/sendmsg", msg,
    #                       content_type="application/json")
    #     self.assertEqual(rep.status_code, 200)
    #     data = json.loads(rep.content)
    #     self.assertEqual(data['msg'], STATUS_CODE['Success'])

    def test_send_tel_with_letter(self):
        '''测试电话号码中有字母'''
        client = Client()
        msg = {"tel": "2222333345a",
               "dmac": "ff:ff:ff:ff:ff:ff"}
        rep = client.post("/api/sendmsg", msg, content_type="application/json")
        self.assertEqual(rep.status_code, 200)
        data = json.loads(rep.content)
        self.assertEqual(data['msg'], STATUS_CODE['Error Tel Number'])

    def test_send_short_tel(self):
        '''测试电话号码过短'''
        client = Client()
        msg = {"tel": "222333",
               "dmac": "ff:ff:ff:ff:ff:ff"}
        rep = client.post("/api/sendmsg", msg, content_type="application/json")
        self.assertEqual(rep.status_code, 200)
        data = json.loads(rep.content)
        self.assertEqual(data['msg'], STATUS_CODE['Error Tel Number'])

    def test_send_tel(self):
        '''测试测试电话号码过短'''
        client = Client()
        msg = {"tel": "12324",
               "dmac": "ff:ff:ff:ff:ff:ff"}
        rep = client.post("/api/sendmsg", msg, content_type="application/json")
        self.assertEqual(rep.status_code, 200)
        data = json.loads(rep.content)
        self.assertEqual(data['msg'], STATUS_CODE['Error Tel Number'])


class ChangePasswordTestCase(TestCase):
    '''测试修改密码的类'''

    def setUp(self):
        user1 = User(username='user1')
        user1.set_password('user1')
        user1.save()
        user2 = User(username='user2')
        user2.set_password('user2')
        user2.save()

    def test_correct(self):
        '''测试原密码正确'''
        client = Client()
        client.login(username='user1', password='user1')
        data = {
            'username': 'user1',
            'old_psw': 'user1',
            'new_psw': 'change',
        }
        rep = client.post('/api/change_password', data,
                          content_type='application/json')
        content = json.loads(rep.content)
        self.assertEqual(rep.status_code, 200)
        self.assertTrue(content['error'] == STATUS_CODE['Success'])

    def test_error(self):
        '''测试原密码错误'''
        client = Client()
        client.login(username='user2', password='user2')
        data = {
            'username': 'user2',
            'old_psw': 'user1',
            'new_psw': 'change',
        }
        rep = client.post('/api/change_password', data,
                          content_type='application/json')
        content = json.loads(rep.content)
        self.assertEqual(rep.status_code, 200)
        self.assertTrue(content['error'] == STATUS_CODE['Password Not Match'])


class GetSellRecordsTestCase(TestCase):
    '''本类用于测试返回地推人员销售信息'''

    def setUp(self):
        user_sel = User.objects.create(
            username='seller1', user_type=USER_TYPE['seller'])
        user_sel.set_password('seller1')
        user_sel.save()
        seller = SellerInfo.objects.create(
            seller=user_sel, city="Beijing", price=29.98)
        user_cus = User.objects.create(
            username='customer1', password='customer1',
            user_type=USER_TYPE['customer'])
        customer = Customer.objects.create(user=user_cus)
        SellRecord.objects.create(
            customer=customer, seller=seller, money=29.98)
        SellRecord.objects.create(
            customer=customer, seller=seller, money=39.98)

    def test_get_records(self):
        '''
        本方法用于检测获取销售记录
        '''
        today = datetime.now()
        tomorrow = today + timedelta(hours=23, minutes=59, seconds=59)
        tomorrow = tomorrow.strftime("%Y-%m-%d")
        client = Client()
        client.login(username='seller1', password='seller1')
        data = {
            'username': 'seller1',
            'date0': '2018-08-08',
            'date1': tomorrow
        }
        rep = client.post('/api/get_sellrecords', data,
                          content_type='application/json')
        content = json.loads(rep.content)
        self.assertTrue('today_count' in content['list'][0])
        self.assertTrue('today_money' in content['list'][0])
        self.assertTrue('history_count' in content['list'][0])
        self.assertTrue('history_money' in content['list'][0])


class RegisterPayTestCase(TestCase):
    '''测试注册时发送支付请求'''

    def setUp(self):
        user_sel = User.objects.create(
            username='seller1', user_type=USER_TYPE['seller'])
        user_sel.set_password('seller1')
        user_sel.save()
        SellerInfo.objects.create(
            seller=user_sel, city="Beijing", price=29.98)
        user_cus = User.objects.create(
            username='customer1', password='customer1',
            user_type=USER_TYPE['customer'])
        Customer.objects.create(user=user_cus)

    def test_miss_value(self):
        '''测试前端数据异常'''
        client = Client()
        data = {
            'te': 'customer1',
            'child_name': 'child1',
            'seller_id': SellerInfo.objects.filter(
                city="Beijing", price=29.98).first().id
        }
        response = client.post('/api/payviews', data,
                               content_type='application/json')
        content = json.loads(response.content)
        self.assertEqual(content['msg'], STATUS_CODE['Frontend Value Error'])

    def test_not_found_seller(self):
        '''测试没有地推人员'''
        client = Client()
        data = {
            'tel': 'customer1',
            'child_name': 'child1',
            'seller_id': 10086,
        }
        response = client.post('/api/payviews', data,
                               content_type='application/json')
        content = json.loads(response.content)
        self.assertEqual(content['msg'], STATUS_CODE['User Not Found'])

    def test_not_found_customer(self):
        '''测试没有顾客'''
        client = Client()
        data = {
            'tel': '1234567890',
            'child_name': 'child1',
            'seller_id': SellerInfo.objects.filter(
                city="Beijing", price=29.98).first().id
        }
        response = client.post('/api/payviews', data,
                               content_type='application/json')
        content = json.loads(response.content)
        self.assertEqual(content['msg'], STATUS_CODE['User Not Found'])


class CheckMobileTestCase(TestCase):
    '''本类用于测试检查请求来源功能'''

    def setUp(self):
        '''本函数用来初始化'''

    def test_check_mobile(self):
        '''本函数用来测试来源为Pixel 2 手机端时的Check'''
        mobile_user_agent = (
            'Mozilla/5.0 (Linux; Android 8.0; \
            Pixel 2 Build/OPD3.170816.012) AppleWeb\
            Kit/537.36 (KHTML, like Gecko)\
            Chrome/68.0.3440.106 Mobile Safari/537.36')
        self.assertEqual(check_mobile(mobile_user_agent), True)

    def test_check_pc(self):
        '''本函数用来测试来源为PC端时的Check'''
        pc_user_agent = (
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64)\
             AppleWebKit/537.36 (KHTML, like\
             Gecko) Chrome/68.0.3440.106 Safari/537.36')
        self.assertEqual(check_mobile(pc_user_agent), False)


class CcCheckRefund(TestCase):
    '''本类用于测试课程顾问查看退款情况及处理退款'''

    def setUp(self):
        user = User.objects.create(username='15900001234', password='123')
        teacher1 = Teacher.objects.create(name='teacher1')
        courses = []
        for i in range(3):
            course = Courses.objects.create(
                name='course'+str(i+1), teacher_id=teacher1, total_sec=48,
                date=1, time='8:00:00')
            courses.append(course)
        counts = [12, 19, 31]
        dates = ['2018-07-02', '2018-08-06', '2018-05-29']
        for i in range(3):
            Section.objects.create(
                course_id=courses[i], count=counts[i], date=dates[i],
                start_time='08:00', end_time='10:00', is_cancel=True)
        customer = Customer(user=user, child_name='child1')
        customer.save()
        consult = User.objects.create(
            username='cc', user_type=USER_TYPE['consultant'])
        consult.set_password('cc')
        consult.save()
        for i in range(3):
            CcRecord.objects.create(
                customer=customer, cc=consult, money=4396, course=courses[i])
        RefundRecord.objects.create(
            customer=customer, course=courses[0], refund=4396, cc=consult,
            date='2018-07-05 10:00:00', deal_date='2018-08-10 08:00:00',
            is_passed=True, is_paid=True, reason='too difficult')
        RefundRecord.objects.create(
            customer=customer, course=courses[1], cc=consult,
            date='2018-08-07 19:00:00', is_passed=False,
            is_paid=False, reason='the time does not fit')
        RefundRecord.objects.create(
            customer=customer, course=courses[2], refund=4396, cc=consult,
            date='2018-08-01 15:00:00', deal_date='2018-08-10 08:00:00',
            is_passed=True, is_paid=False, reason='do not like')

    def test_check_true_refund(self):
        '''测试查看近30天已处理的退费记录'''
        client = Client()
        client.login(username='cc', password='cc')
        data = {
            'username': 'cc',
            'refund': True
        }
        rep = client.post('/api/cc_check_refund', data,
                          content_type='application/json')
        content = json.loads(rep.content)
        self.assertEqual(rep.status_code, 200)
        self.assertEqual(content['list'][0]['cncl_num'], 12)
        self.assertEqual(content['list'][1]['cncl_num'], 31)

    def test_check_false_refund(self):
        '''测试查看没有处理的退费记录'''
        client = Client()
        client.login(username='cc', password='cc')
        data = {
            'username': 'cc',
            'refund': False
        }
        rep = client.post('/api/cc_check_refund', data,
                          content_type='application/json')
        content = json.loads(rep.content)
        self.assertEqual(rep.status_code, 200)
        self.assertEqual(content['list'][0]['cncl_num'], 19)

    def test_ensure_refund(self):
        '''测试处理退款'''
        client = Client()
        client.login(username='cc', password='cc')
        record = RefundRecord.objects.get(reason='the time does not fit')
        data = {
            'id': record.id,
            'refund': '2500'
        }
        rep = client.post('/api/cc_ensure_refund', data,
                          content_type='application/json')
        record = RefundRecord.objects.get(reason='the time does not fit')
        content = json.loads(rep.content)
        self.assertEqual(rep.status_code, 200)
        self.assertEqual(record.refund, 2500)
        self.assertEqual(record.is_passed, True)
        self.assertEqual(content['error'], STATUS_CODE['Success'])


class CcTestCase(TestCase):
    '''本函数用来测试查看课程顾问业绩功能'''

    def setUp(self):
        '''本函数用来初始化'''
        customer = User.objects.create(
            username='customer', user_type=USER_TYPE['customer'])
        customer.set_password('321')
        customer.save()
        consult = User.objects.create(
            username="cc", user_type=USER_TYPE['consultant'])
        consult.set_password('123')
        consult.save()
        for i in range(3):
            cer = Customer.objects.create(
                user=customer,
                child_name='child' + str(i),
                date_cc=(
                    datetime.strptime("2018-08-12", "%Y-%m-%d") +
                    i*timedelta(days=1)
                ),
                cc=consult,
                audition_count=i,
                is_paid=True
            )
            cer.save()
            if i > 0:
                cer.is_signedup = True
                cer.save()
                CcRecord.objects.create(
                    customer=cer,
                    cc=consult,
                    money=i*100,
                    date=datetime.strptime("2018-08-14", "%Y-%m-%d") +
                    i*timedelta(days=1),
                    info='test'+str(i),
                    course=get_course()
                ).save()

    def test_view_customers(self):
        '''测试cc查看家长'''
        client = Client()
        client.login(username='cc', password='123')
        response = client.post(
            '/api/cc_view_customers',
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)

    def test_view_ccrecord_success(self):
        '''测试cc查看业绩成功情况'''
        client = Client()
        client.login(username='cc', password='123')
        response = client.post(
            '/api/view_ccrecords',
            {
                'username': 'cc',
                'date_from': '2018-08-12',
                'date_to': '2018-08-16'
            },
            content_type='application/json'
        )
        data = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['msg'], STATUS_CODE['Success'])

    def test_view_ccrecord_wrong(self):
        '''测试cc查看业绩时间段错误情况'''
        client = Client()
        client.login(username='cc', password='123')
        response = client.post(
            '/api/view_ccrecords',
            {
                'username': 'cc',
                'date_from': '2018-08-12',
            },
            content_type='application/json'
        )
        data = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['msg'], STATUS_CODE['Error Time Range'])


class CcSignupInfo(TestCase):
    '''本类用于测试课程顾问填写报名信息'''

    def setUp(self):
        consult = User.objects.create(
            username="cc", user_type=USER_TYPE['consultant'])
        consult.set_password('123')
        consult.save()
        old_user = User.objects.create(username='13801231111', password='1')
        Customer.objects.create(
            user=old_user, child_name='old_child')
        user = User.objects.create(username='17750126548', password='2')
        Customer.objects.create(user=user, child_name='child')

    def test_success_info(self):
        '''测试输入信息正确无误'''
        client = Client()
        client.login(username='cc', password='123')
        data = {
            'tel': '17750126548',
            'child_name': 'child',
            'parent_name': 'parent',
            'classin_id': '123456',
            'classin_name': 'name',
            'birthday': '2011-11-11',
            'old_user': '13801231111',
            'money': '2999.9',
            'day1': '星期五',
            'time1': '18:00-20:00',
            'day2': '星期六',
            'time2': '8:00-12:00',
            'day3': '星期日',
            'time3': '14:00-18:00',
            'demand': '少儿班'
        }
        rep = client.post(
            '/api/cc_signup_info', data,
            content_type='application/json'
        )
        content = json.loads(rep.content)
        self.assertEqual(rep.status_code, 200)
        self.assertEqual(content['error'], STATUS_CODE['Success'])

    def test_error1_info(self):
        '''测试用户不存在的情况'''
        client = Client()
        client.login(username='cc', password='123')
        data = {
            'tel': '17750126544',
        }
        rep = client.post(
            '/api/cc_signup_info', data,
            content_type='application/json'
        )
        content = json.loads(rep.content)
        self.assertEqual(rep.status_code, 200)
        self.assertEqual(content['error'], STATUS_CODE['User Not Found'])

    def test_error2_info(self):
        '''测试孩子信息不匹配的情况'''
        client = Client()
        client.login(username='cc', password='123')
        data = {
            'tel': '17750126548',
            'child_name': 'nochild'
        }
        rep = client.post(
            '/api/cc_signup_info', data,
            content_type='application/json'
        )
        content = json.loads(rep.content)
        self.assertEqual(rep.status_code, 200)
        self.assertEqual(content['error'], STATUS_CODE['Child Not Found'])

    def test_error3_info(self):
        '''测试老客户信息不存在的情况'''
        client = Client()
        client.login(username='cc', password='123')
        data = {
            'tel': '17750126548',
            'child_name': 'child',
            'parent_name': 'parent',
            'classin_id': '123456',
            'classin_name': 'name',
            'birthday': '2011-11-11',
            'old_user': '13801231112',
        }
        rep = client.post(
            '/api/cc_signup_info', data,
            content_type='application/json'
        )
        content = json.loads(rep.content)
        self.assertEqual(rep.status_code, 200)
        self.assertEqual(content['error'], STATUS_CODE['Old Not Found'])


class SuperuserRegisterTestCase(TestCase):
    '''本类用于超级管理员注册员工'''

    def setUp(self):
        superuser = User.objects.create(
            username='superuser', user_type=USER_TYPE['superuser'])
        superuser.set_password('superuser')
        superuser.save()
        user = User.objects.create(
            username='cc', user_type=USER_TYPE['consultant'])
        user.set_password('cc')
        user.save()

    def test_success_regist(self):
        '''测试用户名没有重复'''
        client = Client()
        client.login(username='superuser', password='superuser')
        data = {
            'username': 'eduadmin',
            'password': 'eduadmin',
            'user_type': USER_TYPE['eduadmin'],
            'gender': 'woman',
            'email': '123456789@qq.com'
        }
        rep = client.post('/api/superuser_register', data,
                          content_type='application/json')
        User.objects.filter(username='eduadmin')
        content = json.loads(rep.content)
        self.assertEqual(rep.status_code, 200)
        self.assertEqual(content['error'], STATUS_CODE['Success'])

    def test_error_register(self):
        '''测试用户名重复'''
        client = Client()
        client.login(username='superuser', password='superuser')
        data = {
            'username': 'cc',
            'password': 'cc',
            'user_type': USER_TYPE['consultant'],
            'gender': 'man',
            'email': '123456789@qq.com'
        }
        rep = client.post('/api/superuser_register', data,
                          content_type='application/json')
        content = json.loads(rep.content)
        self.assertEqual(rep.status_code, 200)
        self.assertEqual(content['error'], STATUS_CODE['User Already Exists'])


class SuperuserImportTestCase(TestCase):
    '''本类用于超级管理员导入数据功能'''

    def setUp(self):
        '''本函数用来初始化'''
        user = User.objects.create(
            username='cc', user_type=USER_TYPE['consultant'])
        user.set_password('cc')
        user.save()

    def test_check_import_frontend_error(self):
        '''测试前端数据错误时'''
        client = Client()
        client.login(username='cc', password='cc')
        response = client.post(
            '/api/sup_import_customer',
            content_type='application/json'
        )
        data = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['msg'], STATUS_CODE['Frontend Value Error'])


class SuperuserModifyTestCase(TestCase):
    '''本类用于超级管理员查看和修改用户数据功能'''

    def setUp(self):
        '''本函数用来初始化'''
        superuser = User.objects.create(
            username='superuser', user_type=USER_TYPE['superuser'])
        superuser.set_password('superuser')
        superuser.save()
        user = User.objects.create(
            username='customer', user_type=USER_TYPE['customer'])
        user.set_password('customer')
        user.save()
        User.objects.create(
            username='cc', user_type=USER_TYPE['consultant']).save()
        User.objects.create(
            username='other_customer', user_type=USER_TYPE['customer']).save()
        Customer.objects.create(user=user, child_name='child1').save()
        customer = Customer.objects.create(user=user, child_name='child2')
        customer.save()
        self.customer_id = customer.id

    def test_modify_customer_info(self):
        '''本函数用来测试修改客户信息'''
        client = Client()
        client.login(username='superuser', password='superuser')
        customer_id = search_customer('customer', 'child1')[0].id
        response = client.post(
            '/api/modify_customer',
            {
                'customer_id': customer_id,
                'user': 'other_customer',
                'child_name': 'modify_child',
                'parent_name': 'modify_parent',
                'class_id': 'modify_classinid',
                'classin_name': 'modify_classin_name',
                'birthday': '1998-08-28',
                'cc': 'cc',
                'audition_count': 2,
                'old_user_username': 'customer',
                'old_user_child': 'child2',
                'date_cc': '2011-02-02'
            },
            content_type='application/json'
        )
        data = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['msg'], STATUS_CODE['Success'])

    def test_modify_user_info(self):
        '''本函数用来测试改用户信息'''
        client = Client()
        client.login(username='superuser', password='superuser')
        response = client.post(
            '/api/modify_user',
            {
                'username': 'cc',
                'password': '123',
                'email': 'test@email',
                'user_type': USER_TYPE['superuser'],
                'gender': '男',
            },
            content_type='application/json'
        )
        data = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['msg'], STATUS_CODE['Success'])

    def test_view_users(self):
        '''本函数用来测试查看用户信息'''
        client = Client()
        client.login(username='superuser', password='superuser')
        response = client.post(
            '/api/sup_view_users',
            {
                'username': '',
                'user_type': USER_TYPE['customer'],
            },
            content_type='application/json'
        )
        data = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['msg'], STATUS_CODE['Success'])

    def test_view_customers(self):
        '''本函数用来测试查看客户信息'''
        client = Client()
        client.login(username='superuser', password='superuser')
        response = client.post(
            '/api/sup_view_customers',
            {
                'username': 'customer',
            },
            content_type='application/json'
        )
        data = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['msg'], STATUS_CODE['Success'])

    def test_delete_user_empty(self):
        '''本函数用来测试管理员删除用户数据不全时'''
        client = Client()
        client.login(username='superuser', password='superuser')
        response = client.post(
            '/api/delete_user',
            content_type='application/json'
        )
        data = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['msg'], STATUS_CODE['Frontend Value Error'])

    def test_delete_customer_empty(self):
        '''本函数用来测试管理员删除客户数据不全时'''
        client = Client()
        client.login(username='superuser', password='superuser')
        response = client.post(
            '/api/delete_customer',
            content_type='application/json'
        )
        data = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['msg'], STATUS_CODE['Frontend Value Error'])

    def test_delete_user_success(self):
        '''本函数用来测试管理员删除用户成功功能'''
        client = Client()
        client.login(username='superuser', password='superuser')
        response = client.post(
            '/api/delete_user',
            {
                'username': 'cc',
            },
            content_type='application/json'
        )
        data = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['msg'], STATUS_CODE['Success'])

    def test_delete_customer_success(self):
        '''本函数用来测试管理员删除客户户成功功能'''
        client = Client()
        client.login(username='superuser', password='superuser')
        response = client.post(
            '/api/delete_customer',
            {
                'customer_id': self.customer_id,
            },
            content_type='application/json'
        )
        data = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['msg'], STATUS_CODE['Success'])

    def test_check_import(self):
        '''测试超级管理员身份不符合时'''
        client = Client()
        client.login(username='customer', password='customer')
        for url in ['modify_customer', 'modify_user',
                    'delete_user', 'delete_customer']:
            response = client.post(
                '/api/'+url,
                content_type='application/json'
            )
            data = json.loads(response.content)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(data['msg'], STATUS_CODE['Identity Error'])
