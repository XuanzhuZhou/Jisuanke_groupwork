# pragma: no cover
'''本文件暂时用于模拟数据，方便前后端连接测试'''
import os
import sys
import django
import random
import time
os.environ['DJANGO_SETTINGS_MODULE'] = 'server.settings'
django.setup()
from users.models import *
from courses.models import *
from customers.models import *
from datas.models import *
from datetime import date, timedelta, datetime
from statuscode import USER_TYPE, DATE_CODE, LOG_TYPE

os.system('python manage.py migrate')
os.system('python manage.py flush')


def init_teachers_courses():
    """
    本函数用来初始化老师和课程课节
    """
    child_teacher = Teacher.objects.create(
        name='幼儿班老师', tel='15888883214')
    kid_teacher = Teacher.objects.create(
        name='少儿班老师', tel='13699871234')
    child_course = Courses.objects.create(
        name='幼儿围棋课', teacher_id=child_teacher, time='16:00',
        date=DATE_CODE['Saturday'], total_sec=48, price=2999)
    kid_course = Courses.objects.create(
        name='少儿围棋课', teacher_id=kid_teacher, time='10:00',
        date=DATE_CODE['Sunday'], total_sec=48, price=4899)
    child_course_start = datetime.strptime('2018-8-4', "%Y-%m-%d")
    kid_course_start = datetime.strptime('2018-8-5', "%Y-%m-%d")
    for i in range(48):
        Section.objects.create(
            course_id=child_course, count=i+1,
            name='幼儿围棋课'+'<'+str(i+1)+'>',
            date=child_course_start+timedelta(hours=24*7*i),
            start_time='16:00', end_time='18:00',
            location='classIn105')
        Section.objects.create(
            course_id=kid_course, count=i+1,
            name='少儿围棋课'+'<'+str(i+1)+'>',
            date=kid_course_start+timedelta(hours=24*7*i),
            start_time='10:00', end_time='12:00',
            location='classIn108')
    for section in Section.objects.filter(count__lte=3):
        section.is_cancel = True
        section.save()


def init_users_and_records():
    """
    本函数用来初始化user和相关记录
    """

    '''初始化一个超级管理员'''
    superuser = User.objects.create(
        username='superuser', user_type=USER_TYPE['superuser'])
    superuser.set_password('superuser')
    superuser.save()

    '''初始化一个教务'''
    eduadmin = User.objects.create(
        username='eduadmin', user_type=USER_TYPE['eduadmin']
    )
    eduadmin.set_password('eduadmin')
    eduadmin.save()

    '''初始化家长及相关注册、试听、报名记录，课顾，sell地推'''
    citys = ['北京', '上海', '广州', '深圳', '天津', '上海', '石家庄',
             '上海', '天津', '北京', '广州', '成都', '成都', '郑州', '郑州',
             '北京', '石家庄', '北京', '天津', '重庆']
    for i in range(20):

        cus_psw = 100000+i
        user_customer = User.objects.create(
            username='15807'+str(cus_psw), user_type=USER_TYPE['customer'])
        user_customer.set_password(str(cus_psw))
        user_customer.save()
        customer = Customer.objects.create(
            user=user_customer, child_name='child'+str(i+1))

        consultant = User.objects.create(
            username='cc'+str(i+1), user_type=USER_TYPE['consultant'])
        consultant.set_password('cc'+str(i+1))
        consultant.save()

        seller = User.objects.create(
            username='seller'+str(i+1), user_type=USER_TYPE['seller'])
        seller.set_password('seller'+str(i+1))
        seller.save()
        SellerInfo.objects.create(
            seller=seller, city=citys[i],
            price=round(random.uniform(19, 49), 2))
        sellerinfo = SellerInfo.objects.get(pk=random.randint(1, i+1))
        sell_money = sellerinfo.price
        year = random.randint(0, 1)
        month = random.randint(0, 7)
        day = random.randint(0, 20)
        random_date = datetime.now() - timedelta(
            hours=(year*365+month*30+day)*24)
        trade_no = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
        trade_no += ''.join([str(random.randint(0, 9)) for i in range(0, 5)])
        SellRecord.objects.create(
            customer=customer, seller=sellerinfo, money=sell_money,
            date=random_date, trade_no=trade_no)

        is_audition = random.randint(0, 1)
        is_signedup = random.randint(0, 1)
        audition_date = random_date + timedelta(hours=random.randint(1, 5))
        if is_audition == 1:
            audition = AuditionRecord.objects.create(
                customer=customer, section=Section.objects.get(pk=(day+1)),
                date=audition_date)
            if is_signedup == 1:
                audition.is_signedup = True
                audition.save()
                course_choice = random.randint(1, 2)
                course = Courses.objects.get(pk=course_choice)
                consult = User.objects.get(
                    username='cc'+str(random.randint(1, i+1)))
                ccrecord = CcRecord.objects.create(
                    customer=customer, cc=consult, money=course.price,
                    date=audition_date, info='弈学园围棋课',
                    trade_no=trade_no, course=course)
                is_paid = random.randint(0, 1)
                if is_paid == 1:
                    ccrecord.is_paid = True
                    ccrecord.save()


def init_refund_records():
    '''初始化退款记录'''
    User.objects.create(username='refundparent',
                        user_type=USER_TYPE['customer'])
    User.objects.create(username='other', user_type=USER_TYPE['customer'])
    course1 = Courses.objects.get(pk=1)
    course2 = Courses.objects.get(pk=2)
    for i in range(2):
        cer = Customer.objects.create(
            user=User.objects.get(username='refundparent'),
            child_name=('refundchild'+str(i+1)),
            parent_name='refundparent',
            cc=User.objects.get(username='cc1'),
            is_paid=True)
        if i == 0:
            cer.takes.set(Courses.objects.all()[:])
            CcRecord.objects.create(
                customer=cer, cc=User.objects.get(username='cc1'),
                money=8999, info='幼儿围棋课', trade_no=1, course=course1)
            CcRecord.objects.create(
                customer=cer, cc=User.objects.get(username='cc1'),
                money=9999, info='少儿围棋课', trade_no=2, course=course2)
            CcRecord.objects.create(
                customer=cer, cc=User.objects.get(username='cc1'),
                money=9999, info='少儿围棋课', trade_no=2, course=course2)
        else:
            cer.takes.set(Courses.objects.all()[1:])
            CcRecord.objects.create(
                customer=cer, cc=User.objects.get(username='cc1'),
                money=9999, info='少儿围棋课', trade_no=3, course=course2)
        cer.is_signedup = True
        cer.audition_count = i
        cer.save()
    other = Customer.objects.create(
        user=User.objects.get(username='other'),
        child_name='otherchild',
        parent_name='other',
        cc=User.objects.get(username='cc1'))
    other.old_user = Customer.objects.get(child_name="child1")
    other.save()
    rerecord1 = RefundRecord.objects.create(
        customer=Customer.objects.get(child_name='refundchild1'),
        course=Courses.objects.get(pk=1),
        refund=4396,
        cc=User.objects.get(username='cc1'),
        date='2018-07-05 10:00:00',
        deal_date='2018-08-10 08:00:00',
        is_passed=True,
        is_paid=True,
        reason='太难了'
    )
    rerecord2 = RefundRecord.objects.create(
        customer=Customer.objects.get(child_name='refundchild2'),
        course=Courses.objects.get(pk=2),
        cc=User.objects.get(username='cc1'),
        date='2018-08-07 19:00:00',
        is_passed=False,
        is_paid=False,
        reason='时间不合适'
    )
    rerecord3 = RefundRecord.objects.create(
        customer=Customer.objects.get(child_name='refundchild1'),
        course=Courses.objects.get(pk=2),
        refund=4396,
        cc=User.objects.get(username='cc1'),
        date='2018-06-01 15:00:00',
        deal_date='2018-07-10 08:00:00',
        is_passed=True,
        is_paid=True,
        reason='孩子不喜欢'
    )


def init_log():
    '''初始化日志记录'''
    superuser = User.objects.get(username='superuser')
    eduadmin = User.objects.get(username='eduadmin')
    log0 = OperationLogs.objects.create(
        operator=eduadmin, type=LOG_TYPE['Refund'],
        username='child1', info=eduadmin.username+"同意学员child1退费")
    log1 = OperationLogs.objects.create(
        operator=superuser, type=LOG_TYPE['Delete User'],
        username='person1', info=superuser.username+"删除了员工person1")
    log2 = OperationLogs.objects.create(
        operator=superuser, type=LOG_TYPE['Delete Customer'],
        username='person2', info=superuser.username+"删除了用户person2")
    log3 = OperationLogs.objects.create(
        operator=superuser, type=LOG_TYPE['Add User'],
        username='person3', info=superuser.username+"注册了员工person3")


def init_week_grades():
    '''模拟最近七天业绩相关数据'''
    seller = User.objects.create(
        username='周伟', user_type=USER_TYPE['seller'])
    seller.set_password('zhouwei')
    seller.save()
    seller_info = SellerInfo.objects.create(
        seller=seller, city='洛阳', price=29.9)
    user_cus = User.objects.create(username='15903915467')
    consults = User.objects.create(
        username='张康', user_type=USER_TYPE['consultant'])
    consults.set_password('zhangkang')
    consults.save()
    for i in range(20):
        customer = Customer.objects.create(
            user=user_cus, child_name='toaudchild'+str(i))
        customer.cc = consults
        date = datetime.now()
        customer.date_cc = date
        customer.audition_count += 1
        customer.save()
        SellRecord.objects.create(customer=Customer.objects.get(
            child_name='toaudchild'+str(i)), seller=seller_info, money=29.9,
            date=datetime.now())
        AuditionRecord.objects.create(customer=Customer.objects.get(
            child_name='toaudchild'+str(i)),
            date=datetime.now())
    for i in range(9):
        customer = Customer.objects.get(child_name='toaudchild'+str(i))
        customer.is_signedup = True
        customer.is_paid = True
        customer.save()
        date = datetime.now()
        CcRecord.objects.create(
            customer=customer, money=2999.9, is_paid=True,
            date=date, cc=consults)
    for i in range(190):
        Customer.objects.create(user=user_cus, child_name='weaudchild'+str(i))
    num = 0
    for i in range(6):
        sell_count = random.randint(15, 30)
        audition_count = sell_count-random.randint(4, 6)
        sign_count = audition_count-random.randint(1, 6)
        j_num = num
        for j in range(sell_count):
            customer = Customer.objects.get(child_name='weaudchild'+str(j_num))
            customer.cc = consults
            date = datetime.now()-timedelta(hours=(i+1)*24)
            customer.date_cc = date
            customer.save()
            SellRecord.objects.create(
                customer=customer, seller=seller_info, money=29.9, date=date)
            j_num += 1
        k_num = num
        for k in range(audition_count):
            customer = Customer.objects.get(child_name='weaudchild'+str(k_num))
            customer.audition_count += 1
            customer.save()
            AuditionRecord.objects.create(customer=Customer.objects.get(
                child_name='weaudchild'+str(k_num)),
                date=datetime.now()-timedelta(hours=(i+1)*24))
            k_num += 1
        l_num = num
        for l in range(sign_count):
            customer = Customer.objects.get(child_name='weaudchild'+str(l_num))
            customer.is_signedup = True
            customer.is_paid = True
            customer.save()
            CcRecord.objects.create(
                customer=customer, money=2999.9, is_paid=True,
                date=datetime.now()-timedelta(hours=(i+1)*24), cc=consults)
            l_num += 1
        num += sell_count
        num += 1


def init_month_grades():
    '''模拟每个月地推业绩相关数据'''
    seller = User.objects.get(
        username='周伟', user_type=USER_TYPE['seller'])
    seller_info = SellerInfo.objects.get(
        seller=seller, city='洛阳', price=29.9)
    user_cus = User.objects.get(username='15903915467')
    cur_month = date.today().month
    consults = User.objects.get(
        username='张康', user_type=USER_TYPE['consultant'])
    for i in range(400):
        Customer.objects.create(user=user_cus, child_name='mochild'+str(i))
    num = 0
    for i in range(cur_month-1):
        sell_count = random.randint(27, 47)
        audition_count = sell_count-random.randint(5, 10)
        sign_count = audition_count-random.randint(5, 10)
        j_num = num
        for j in range(sell_count):
            customer = Customer.objects.get(child_name='mochild'+str(j_num))
            date_cc = datetime.now()-timedelta(hours=(i+1)*24*30)
            customer.cc = consults
            customer.date_cc = date_cc
            customer.save()
            SellRecord.objects.create(
                customer=customer, seller=seller_info,
                money=29.9, date=date_cc)
            j_num += 1
        k_num = num
        for k in range(audition_count):
            customer = Customer.objects.get(child_name='mochild'+str(k_num))
            customer.audition_count += 1
            customer.save()
            AuditionRecord.objects.create(customer=Customer.objects.get(
                child_name='mochild'+str(k_num)),
                date=datetime.now()-timedelta(hours=(i+1)*24*30))
            k_num += 1
        l_num = num
        for l in range(sign_count):
            customer = Customer.objects.get(child_name='mochild'+str(l_num))
            customer.is_signedup = True
            customer.is_paid = True
            customer.save()
            CcRecord.objects.create(customer=Customer.objects.get(
                child_name='mochild'+str(l_num)), money=2999.9, is_paid=True,
                date=datetime.now()-timedelta(hours=(i+1)*24*30), cc=consults)
            l_num += 1
        num += sell_count
        num += 1


def init_lastyear_grades():
    '''模拟去年的数据'''
    seller = User.objects.get(
        username='周伟', user_type=USER_TYPE['seller'])
    seller_info = SellerInfo.objects.get(
        seller=seller, city='洛阳', price=29.9)
    user_cus = User.objects.get(username='15903915467')
    consults = User.objects.get(
        username='张康', user_type=USER_TYPE['consultant'])
    for i in range(500):
        Customer.objects.create(user=user_cus, child_name='yearchild'+str(i))
    sell_count = 499
    audition_count = sell_count-random.randint(70, 111)
    sign_count = audition_count-random.randint(39, 111)
    for j in range(sell_count):
        customer = Customer.objects.get(child_name='yearchild'+str(j))
        customer.cc = consults
        date_cc = datetime.now()-timedelta(hours=24*365)
        customer.date_cc = date_cc
        customer.save()
        SellRecord.objects.create(
            customer=customer, seller=seller_info, money=29.9, date=date_cc)
    for k in range(audition_count):
        customer = Customer.objects.get(child_name='yearchild'+str(k))
        customer.audition_count += 1
        customer.save()
        AuditionRecord.objects.create(customer=Customer.objects.get(
            child_name='yearchild'+str(k)),
            date=datetime.now()-timedelta(hours=24*365))
    for l in range(sign_count):
        customer = Customer.objects.get(child_name='mochild'+str(l))
        customer.is_signedup = True
        customer.is_paid = True
        CcRecord.objects.create(customer=Customer.objects.get(
            child_name='mochild'+str(l)), money=2999.9, is_paid=True,
            date=datetime.now()-timedelta(hours=24*365), cc=consults)


if __name__ == '__main__':
    init_teachers_courses()
    init_users_and_records()
    init_refund_records()
    init_log()
    init_week_grades()
    init_month_grades()
    init_lastyear_grades()
