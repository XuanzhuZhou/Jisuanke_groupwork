# -*- coding: utf-8 -*-

'''本文件用于建立家长模型'''
from django.db import models

from courses.models import Courses
from statuscode import STATUS_CODE
from users.models import User

# Create your models here.


class Customer(models.Model):
    '''
    保存家长信息的类

    :字段解释:
    + GENDER_CHOICES: 性别选择项 'male': 男 'female' : 女
    + user: 家长所注册用户对象 User
    + child_name: 孩子姓名 CharField max_length=20
    + parent_name: 家长姓名 CharField max_length=20
    + classin_id: class in 账号 CharField max_length=20
    + classin_name: class in 昵称 CharField max_length=20
    + birthday: 孩子生日 DateField
    + cc: 课程顾问 User 外键
    + audition_count: 试听次数 IntegerField
    + is_signedup: 是否报名 BooleanField
    + old_user: 老客户 Customer 外键
    + takes: 报名课程 ManyToManyField Courses
    + date_cc: 分配date_cc 的时间
    + damand: 选课意向
    + gender: 性别 CharField
    '''
    GENDER_CHOICES = (
        ("male", u"男"),
        ("female", u"女"),
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='customer')
    child_name = models.CharField(max_length=20)
    parent_name = models.CharField(max_length=20, null=True, blank=True)
    classin_id = models.CharField(max_length=20, null=True, blank=True)
    classin_name = models.CharField(max_length=20, null=True, blank=True)
    birthday = models.DateField(null=True, blank=True)
    cc = models.ForeignKey(User, related_name='cc_customers',
                           on_delete=models.SET_NULL, null=True)
    audition_count = models.IntegerField(default=0)
    is_signedup = models.BooleanField(default=False)
    is_paid = models.BooleanField(default=False)
    old_user = models.ForeignKey(
        'self', blank=True, null=True, on_delete=models.SET_NULL)
    takes = models.ManyToManyField(
        Courses, related_name='taken', blank=True)
    date_cc = models.DateField(null=True, blank=True)
    demand = models.TextField(max_length=500, blank=True, null=True)
    gender = models.CharField(
        max_length=6, choices=GENDER_CHOICES, null=True, blank=True)

    def __str__(self):
        return self.user.username + ' ' + self.child_name


def get_info(username) -> list:
    """
    本函数用来返回用户名下家长信息

    :前端传入数据: username

    :返回数据: list

    """
    info_list = list(
        User.objects.get(username=username).customer.all().values())
    for info_dict in info_list:
        cc_user = User.objects.filter(id=info_dict['cc_id'])
        if not cc_user.count() == 0:
            info_dict['cc_id'] = cc_user[0].username
        else:
            info_dict['cc_id'] = 'null'
    return info_list


def search_customer(username, child_name=''):
    """
    本函数用来搜索家长

    :前端传入数据: username child_name（默认为''）

    :返回数据: <QuerySet> 或 ''

    """
    try:
        user = User.objects.get(username=username)
        customer = Customer.objects.filter(user=user)
        if child_name != '':
            customer = customer.filter(child_name=child_name)
        return customer
    except User.DoesNotExist:
        return ''


def modify_customer_info(customer_id, form) -> str:
    """
    本函数用来修改家长信息

    :前端传入数据: username  form 修改信息字典

    :返回数据: 状态码 0或902

    """
    customer = Customer.objects.get(id=customer_id)
    msg = STATUS_CODE['Success']
    user_attr = ['cc', 'user']
    for key in user_attr:
        if key in form and form[key] != '':
            try:
                user = User.objects.get(username=form[key])
                setattr(customer, key, user)
            except User.DoesNotExist:
                msg = STATUS_CODE['User Not Found']
            del form[key]
    if 'old_user_username' in form and 'old_user_child' in form:
        old_user = search_customer(
            form['old_user_username'],
            form['old_user_child']
        )
        if old_user.count() > 0 and old_user != '':
            customer.old_user = old_user[0]
    if 'takes' in form:
        del form['takes']
    for key in form.keys():
        if hasattr(customer, key) and form[key] != '':
            setattr(customer, key, form[key])
    customer.save()
    return msg
