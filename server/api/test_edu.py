# -*- coding: utf-8 -*-

'''本文件用于测试'''


import json

from django.test import Client, TestCase

from courses.models import Courses, Section, Teacher
from customers.models import Customer
from datas.models import CcRecord, RefundRecord
from users.models import User

from statuscode import STATUS_CODE, USER_TYPE, REFUND_STATUS


class EduGetCoursesTestCase(TestCase):
    '''本类用于测试教务老师搜索并查看课程信息'''

    def setUp(self):
        eduadmin = User.objects.create(username='eduadmin')
        eduadmin.set_password('eduadmin')
        eduadmin.save()
        teacher1 = Teacher.objects.create(name='teacher1')
        teacher2 = Teacher.objects.create(name='teacher2')
        course1 = Courses.objects.create(
            name='course1', teacher_id=teacher1, total_sec=48, date=1,
            time='8:00')
        Courses.objects.create(
            name='course2', teacher_id=teacher1, total_sec=90, date=1,
            time='10:00')
        Courses.objects.create(
            name='course3', teacher_id=teacher1, total_sec=48, date=3,
            time='10:00')
        Courses.objects.create(
            name='course4', teacher_id=teacher2, total_sec=48, date=5,
            time='8:00')
        Section.objects.create(
            course_id=course1, count=1, date='2018-07-31', start_time='8:00',
            end_time='10:00', location='5A')
        Section.objects.create(
            course_id=course1, count=2, date='2018-08-06', start_time='8:00',
            end_time='10:00', location='5A')
        Section.objects.create(
            course_id=course1, count=3, date='2018-08-13', start_time='8:00',
            end_time='10:00', location='5A')
        Section.objects.create(
            course_id=course1, count=4, date='2018-08-20', start_time='8:00',
            end_time='10:00', location='5A')
        user = User.objects.create(
            username='15912340711', password='123',
            user_type=USER_TYPE['customer'])
        customer = Customer(user=user, child_name='child1')
        customer.save()
        customer.takes.set(Courses.objects.all())
        customer.save()
        customer = Customer(user=user, child_name='child2')
        customer.save()
        customer.takes.set(Courses.objects.all())
        customer.save()

    def test_all_info(self):
        '''测试全部搜索信息'''
        client = Client()
        client.login(username='eduadmin', password='eduadmin')
        data = {
            'tel': '15912340711',
            'childname': 'child1',
            'teacher': 'teacher1',
            'day': '1',
            'time': '08:00'
        }
        rep = client.post('/api/eduadmin_get_courses', data,
                          content_type='application/json')
        content = json.loads(rep.content)
        self.assertEqual(rep.status_code, 200)
        self.assertTrue(content['error'] == STATUS_CODE['Success'])
        self.assertTrue('list' in content)

    def test_notall_info(self):
        '''测试搜索信息不完全的情况'''
        client = Client()
        client.login(username='eduadmin', password='eduadmin')
        data = {
            'tel': '15912340711',
            'childname': 'child1',
            'teacher': 'teacher1',
            'day': '',
            'time': ''
        }
        rep = client.post('/api/eduadmin_get_courses', data,
                          content_type='application/json')
        content = json.loads(rep.content)
        self.assertEqual(rep.status_code, 200)
        self.assertTrue(content['error'] == STATUS_CODE['Success'])
        self.assertTrue('list' in content)

    def test_notstudent_info(self):
        '''测试学生信息不匹配的情况'''
        client = Client()
        client.login(username='eduadmin', password='eduadmin')
        data = {
            'tel': '15912340711',
            'childname': 'notchild',
            'teacher': '',
            'day': '',
            'time': ''
        }
        rep = client.post('/api/eduadmin_get_courses', data,
                          content_type='application/json')
        content = json.loads(rep.content)
        self.assertEqual(rep.status_code, 200)
        self.assertTrue(content['error'] == STATUS_CODE['Not Found'])
        self.assertTrue('list' not in content)

    def test_notteacher_info(self):
        '''测试老师信息不匹配的情况'''
        client = Client()
        client.login(username='eduadmin', password='eduadmin')
        data = {
            'tel': '15912340711',
            'childname': 'child2',
            'teacher': 'notteacher',
            'day': '',
            'time': ''
        }
        rep = client.post('/api/eduadmin_get_courses', data,
                          content_type='application/json')
        content = json.loads(rep.content)
        self.assertEqual(rep.status_code, 200)
        self.assertTrue(content['error'] == STATUS_CODE['Not Found'])
        self.assertTrue('list' not in content)


class EduGetCancelTestCase(TestCase):
    '''本类用于测试教务老师查看和确认销课'''

    def setUp(self):
        eduadmin = User.objects.create(username='eduadmin')
        eduadmin.set_password('eduadmin')
        eduadmin.save()
        teacher1 = Teacher.objects.create(name='teacher1')
        course1 = Courses.objects.create(
            name='course1', teacher_id=teacher1, total_sec=48, date=1,
            time='8:00')
        Section.objects.create(
            course_id=course1, count=1,
            date='2018-07-31', start_time='8:00',
            end_time='10:00', location='5A', is_cancel=True)
        Section.objects.create(
            course_id=course1, count=2,
            date='2018-08-06', start_time='8:00',
            end_time='10:00', location='5A')
        Section.objects.create(
            course_id=course1, count=3,
            date='2018-08-13', start_time='8:00',
            end_time='10:00', location='5A', is_cancel=True)
        Section.objects.create(
            course_id=course1, count=4,
            date='2018-08-20', start_time='8:00',
            end_time='10:00', location='5A')

    def test_get_cancell(self):
        '''测试查看近一周销课信息以及所有未销课信息'''
        client = Client()
        client.login(username='eduadmin', password='eduadmin')
        rep = client.post('/api/eduadmin_cancell_courses')
        content = json.loads(rep.content)
        self.assertEqual(rep.status_code, 200)
        self.assertTrue('list' in content)

    def test_ensure_cancell(self):
        '''测试确认销课'''
        client = Client()
        client.login(username='eduadmin', password='eduadmin')
        section_id = Section.objects.filter(is_cancel=False)[0].id
        data = {
            'id': section_id
        }
        rep = client.post('/api/eduadmin_ensure_cancell',
                          data, content_type='application/json')
        content = json.loads(rep.content)
        section = Section.objects.get(pk=section_id)
        self.assertEqual(rep.status_code, 200)
        self.assertTrue(section.is_cancel)
        self.assertTrue(content['seccess'])


class EduArrCourTestCase(TestCase):
    '''本类用于测试教务老师安排课程'''

    def setUp(self):
        eduadmin = User.objects.create(username='eduadmin')
        eduadmin.set_password('eduadmin')
        eduadmin.save()
        teacher1 = Teacher.objects.create(name='teacher1')
        course1 = Courses.objects.create(
            name='course1', teacher_id=teacher1, total_sec=48, date=1,
            time='8:00')
        Courses.objects.create(
            name='course2', teacher_id=teacher1, total_sec=90, date=1,
            time='10:00')
        Courses.objects.create(
            name='course3', teacher_id=teacher1, total_sec=48, date=3,
            time='10:00')
        user = User.objects.create(
            username='15912340711', password='123',
            user_type=USER_TYPE['customer'])
        customer = Customer(user=user, child_name='child1')
        customer.save()
        customer.takes.set(Courses.objects.all()[:2])
        customer.save()
        CcRecord.objects.create(customer=customer, money='2999')
        CcRecord.objects.create(
            customer=customer, money='4800', course=course1)

    def test_eduarr_success(self):
        '''验证身份信息正确，课程可选的情况'''
        client = Client()
        client.login(username='eduadmin', password='eduadmin')
        customer = Customer.objects.get(child_name='child1')
        course = Courses.objects.get(name='course3')
        course_id = course.id
        data = {
            'id': course_id,
            'tel': '15912340711',
            'child_name': 'child1',
        }
        customer = Customer.objects.get(child_name='child1')
        rep = client.post('/api/eduadmin_arrange_course', data,
                          content_type='application/json')
        content = json.loads(rep.content)
        self.assertEqual(rep.status_code, 200)
        self.assertEqual(content['error'], STATUS_CODE['Success'])
        self.assertEqual(customer.takes.count(), 2)

    def test_eduarr_chose(self):
        '''验证课程已经被选择的情况'''
        customer = Customer.objects.get(child_name='child1')
        course_id = customer.takes.all()[0].id
        client = Client()
        client.login(username='eduadmin', password='eduadmin')
        data = {
            'id': course_id,
            'tel': '15912340711',
            'child_name': 'child1',
        }
        rep = client.post('/api/eduadmin_arrange_course', data,
                          content_type='application/json')
        content = json.loads(rep.content)
        self.assertEqual(rep.status_code, 200)
        self.assertEqual(content['error'], STATUS_CODE['Not Found'])

    def test_aduarr_telerror(self):
        '''验证tel不存在的情况'''
        client = Client()
        client.login(username='eduadmin', password='eduadmin')
        data = {
            'id': 4,
            'tel': '15912340710',
            'child_name': 'child1',
        }
        rep = client.post('/api/eduadmin_arrange_course', data,
                          content_type='application/json')
        content = json.loads(rep.content)
        self.assertEqual(rep.status_code, 200)
        self.assertEqual(content['error'], STATUS_CODE['Not Found'])

    def test_aduarr_chierror(self):
        '''验证child不存在的情况'''
        client = Client()
        client.login(username='eduadmin', password='eduadmin')
        data = {
            'id': 1,
            'tel': '15912340711',
            'child_name': 'notchild',
        }
        rep = client.post('/api/eduadmin_arrange_course', data,
                          content_type='application/json')
        content = json.loads(rep.content)
        self.assertEqual(rep.status_code, 200)
        self.assertEqual(content['error'], STATUS_CODE['Not Found'])


class EduCheckRefundTestCase(TestCase):
    '''该类用来测试教务老师查询退款信息'''

    def setUp(self):
        '''初始化测试样例数据'''
        edu = User.objects.create(
            username='eduadmin', user_type=USER_TYPE['eduadmin'])
        edu.set_password('adminedu')
        edu.save()
        teachers, courses = [], []
        subjects = ['Math', 'Chinese', 'English', 'Comp']
        times = ['8:00', '10:00', '14:00', '16:00']
        for index in range(4):
            teacher = Teacher.objects.create(name="teacher" + str(index))
            teachers.append(teacher)
        for index in range(4):
            courses.append(Courses.objects.create(
                name=subjects[index], teacher_id=teachers[index],
                total_sec=16, date=index, time=times[index]))
        courses.append(Courses.objects.create(
            name='Math', teacher_id=teachers[0],
            total_sec=16, date=5, time='8:00'))
        user = User.objects.create(username='12345677654', password='123',
                                   user_type=USER_TYPE['customer'])
        for index in range(2):
            child = "child" + str(index + 1)
            customer = Customer.objects.create(user=user, child_name=child)
            customer.takes.set(Courses.objects.all())
            customer.save()
        consultant = User.objects.create(
            username='cc', password='cc', user_type=USER_TYPE['consultant'])
        refunds = [1234, 9012, 1234]
        for index in range(3):
            CcRecord.objects.create(
                customer=customer, cc=consultant,
                money=refunds[index], course=courses[index])
            RefundRecord.objects.create(
                customer=customer, course=courses[index], refund=refunds[0],
                cc=consultant, date='2018-08-07 19:0%d:00' % (index,),
                is_passed=False, is_paid=False,
                reason="the reasen is" + str(index))

    def test_with_course_message_name(self):
        '''测试课程名称的模糊搜索'''
        client = Client()
        client.login(username='eduadmin', password='adminedu')
        data = {
            "course_message": "Ma",
        }
        rep = client.post('/api/eduadmin_check_refund', data,
                          content_type='application/json')
        content = json.loads(rep.content)
        self.assertEqual(rep.status_code, 200)
        self.assertEqual(content['msg'], STATUS_CODE['Success'])
        self.assertTrue('refund_records' in content)

    def test_with_course_message_id(self):
        '''测试课程 id 搜索'''
        client = Client()
        client.login(username='eduadmin', password='adminedu')
        data = {
            "course_message": "1",
        }
        rep = client.post('/api/eduadmin_check_refund', data,
                          content_type='application/json')
        content = json.loads(rep.content)
        self.assertEqual(rep.status_code, 200)
        self.assertEqual(content['msg'], STATUS_CODE['Success'])
        self.assertTrue('refund_records' in content)

    def test_without_course_message(self):
        '''测试请求中缺少信息的返回结果'''
        client = Client()
        client.login(username='eduadmin', password='adminedu')
        rep = client.post('/api/eduadmin_check_refund',
                          content_type='application/json')
        content = json.loads(rep.content)
        self.assertEqual(rep.status_code, 200)
        self.assertEqual(content['msg'], STATUS_CODE['Success'])
        self.assertTrue('refund_records' in content)


class EduEnsureRefundTestCase(TestCase):
    '''本类用来测试教务老师确认退款'''

    def setUp(self):
        '''初始化测试数据'''
        edu = User.objects.create(
            username='eduadmin', user_type=USER_TYPE['eduadmin'])
        edu.set_password('adminedu')
        edu.save()

        teacher1 = Teacher.objects.create(name='teacher1')
        teacher2 = Teacher.objects.create(name='teacher2')
        teacher3 = Teacher.objects.create(name='teacher3')
        teacher4 = Teacher.objects.create(name='teacher4')

        course1 = Courses.objects.create(
            name='Math', teacher_id=teacher1,
            total_sec=16, date=1, time='8:00')
        course2 = Courses.objects.create(
            name='Chinese', teacher_id=teacher2,
            total_sec=16, date=2, time='10:00')
        course3 = Courses.objects.create(
            name='English', teacher_id=teacher3,
            total_sec=16, date=1, time='14:00')
        course4 = Courses.objects.create(
            name='Comp.', teacher_id=teacher4,
            total_sec=16, date=3, time='16:00')
        Courses.objects.create(
            name='Math', teacher_id=teacher1,
            total_sec=16, date=5, time='8:00')
        course6 = Courses.objects.create(
            name='PE', teacher_id=teacher4,
            total_sec=16, date=5, time='16:00')

        user = User.objects.create(
            username='12345677654',
            password='1',
            user_type=USER_TYPE['customer']
        )
        customer1 = Customer(user=user, child_name='childlululu')
        customer1.save()
        customer1.takes.set(Courses.objects.all())
        customer1.save()
        customer = Customer(user=user, child_name='childlalala')
        customer.save()
        customer.takes.set(Courses.objects.all())
        customer.save()
        consultant = User.objects.create(
            username='cc', password='cc', user_type=USER_TYPE['consultant'])
        CcRecord.objects.create(
            customer=customer, cc=consultant, money=1234, course=course1)
        CcRecord.objects.create(
            customer=customer, cc=consultant, money=5678, course=course2)
        CcRecord.objects.create(
            customer=customer, cc=consultant, money=9012, course=course3)
        CcRecord.objects.create(
            customer=customer, cc=consultant, money=1, course=course6)
        RefundRecord.objects.create(
            customer=customer, course=course1, refund=1234,
            cc=consultant, date='2018-08-07 19:00:00', is_passed=True,
            is_paid=False, reason='the time does not fit'
        )
        RefundRecord.objects.create(
            customer=customer, course=course2, refund=1234,
            cc=consultant, date='2018-08-07 19:02:00', is_passed=True,
            is_paid=True, reason='the time does not fit'
        )
        RefundRecord.objects.create(
            customer=customer, course=course3, refund=9012, cc=consultant,
            date='2018-08-07 19:01:00', is_passed=False,
            is_paid=False, reason='不喜欢'
        )
        RefundRecord.objects.create(
            customer=customer, course=course4, refund=9012,
            cc=consultant, date='2018-08-07 19:06:00',
            is_passed=True, is_paid=False, reason='不喜欢'
        )
        RefundRecord.objects.create(
            customer=customer, course=course6,
            refund=10086, cc=consultant, date='2018-08-07 19:08:00',
            is_passed=True, is_paid=False, reason='不需要理由')

    def test_miss_value(self):
        '''测试请求中缺少数据的处理'''
        client = Client()
        client.login(username='eduadmin', password='adminedu')
        rep = client.post('/api/eduadmin_ensure_refund',
                          content_type='application/json')
        content = json.loads(rep.content)
        self.assertEqual(rep.status_code, 200)
        self.assertEqual(content['msg'], STATUS_CODE['Frontend Value Error'])

    def test_not_found_customer(self):
        '''测试给不存在的家长退款'''
        client = Client()
        client.login(username='eduadmin', password='adminedu')
        data = {
            'customer_id':
                Customer.objects.get(child_name='childlalala').id + 1223,
            'course_id':
                Courses.objects.get(name='Math', date=1, time='8:00').id
        }
        rep = client.post('/api/eduadmin_ensure_refund', data,
                          content_type='application/json')
        content = json.loads(rep.content)
        msg = content['msg']
        self.assertEqual(rep.status_code, 200)
        self.assertEqual(msg, STATUS_CODE['Refund Record Exception'])

    def test_not_found_refundrecord(self):
        '''测试对没有退款记录的情况的处理'''
        client = Client()
        client.login(username='eduadmin', password='adminedu')
        data = {
            'customer_id':
                Customer.objects.get(child_name='childlalala').id,
            'course_id':
                Courses.objects.get(name='Math', date=5).id
        }
        rep = client.post('/api/eduadmin_ensure_refund', data,
                          content_type='application/json')
        content = json.loads(rep.content)
        self.assertEqual(rep.status_code, 200)
        self.assertEqual(
            content['msg'], STATUS_CODE['Refund Record Exception'])

    def test_not_found_ccrecord(self):
        '''测试退款记录和 cc 记录不匹配的情况处理'''
        client = Client()
        client.login(username='eduadmin', password='adminedu')
        data = {
            'customer_id':
                Customer.objects.get(child_name='childlalala').id,
            'course_id':
                Courses.objects.get(name='Comp.', date=3).id
        }
        rep = client.post('/api/eduadmin_ensure_refund', data,
                          content_type='application/json')
        content = json.loads(rep.content)
        self.assertEqual(rep.status_code, 200)
        self.assertEqual(content['msg'], STATUS_CODE['Trade Record Exception'])

    def test_is_not_passed(self):
        '''测试对未经课程顾问通过的退款进行确认的处理'''
        client = Client()
        client.login(username='eduadmin', password='adminedu')
        data = {
            'customer_id':
                Customer.objects.get(child_name='childlalala').id,
            'course_id':
                Courses.objects.get(name='English', date=1, time='14:00').id
        }
        response = client.post('/api/eduadmin_ensure_refund', data,
                               content_type='application/json')
        content = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(content['msg'], REFUND_STATUS['Under Review'])

    def test_wrong_price(self):
        '''测试价格错误'''
        client = Client()
        client.login(username='eduadmin', password='adminedu')
        data = {
            'customer_id':
                Customer.objects.get(child_name='childlalala').id,
            'course_id':
                Courses.objects.get(name='PE', date=5).id,
            'refund_account': 999999,
        }
        rep = client.post('/api/eduadmin_ensure_refund', data,
                          content_type='application/json')
        content = json.loads(rep.content)
        self.assertEqual(rep.status_code, 200)
        self.assertEqual(content['msg'], STATUS_CODE['Price Not Match'])
