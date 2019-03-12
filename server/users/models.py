# -*- coding: utf-8 -*-

'''本文件用于建立user数据库模型'''

from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime
from statuscode import STATUS_CODE, USER_TYPE

# Create your models here.


class User(AbstractUser):
    """
    自定义用户类

    :类继承: 自 django.contrib.auth.models.AbstractUser

    :字段信息:

    + USER_TYPE_CHOICES: 身份选择项 详情见statuscode.py

    + GENDER_CHOICES: 性别选择项 'male': 男 'female' : 女

    + username: 用户名  自django

    + password: 密码    自django

    + user_type: 该用户对象的身份  PositiveSmallInteferField

    + gender: 该用户性别 CharField

    """
    # : 用户类型选择列表参照z
    USER_TYPE_CHOICES = (
        (0, 'admin'),
        (1, 'customer'),
        (2, 'superuser'),
        (3, 'consultant'),
        (4, 'eduadmin'),
        (5, 'seller'),
    )
    GENDER_CHOICES = (
        ("male", u"男"),
        ("female", u"女"),
    )
    user_type = models.PositiveSmallIntegerField(
        choices=USER_TYPE_CHOICES, default=0)
    gender = models.CharField(
        max_length=6, choices=GENDER_CHOICES, default="female")

    def __str__(self):
        return ' '.join(
            [self.username, self.get_user_type_display(),
             self.gender, self.email])


class SellerInfo(models.Model):
    """
    地推人员信息类

    :字段解释：

    + seller: 地推人员外键 User

    + city: 城市 CharFiled

    + price: 注册价格 FloatField
    """
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    city = models.CharField(max_length=20)
    price = models.FloatField()


def search_user_info(username, user_type) -> list:
    """
    本函数用于搜索用户信息

    :接受数据： username: 用户名  user_type: 用户类型(参照statuscode USER_TYPE)

    :返回数据: list[dist]

    :返回字典键值: id , password, last_login, is_superuser, username,

    first_name, last_name, email, is_staff, is_active, date_joined,

    user_type, gender

    """
    users = User.objects.filter(user_type=user_type)
    if not username == '':
        users = users.filter(username=username)
    info_list = list(users.values())
    for info in info_list:
        info['date_joined'] = (
            datetime.strftime(info['date_joined'], '%b-%d-%Y %H:%M:%S'))
    return info_list


def modify_user_info(username, form) -> str:
    """
    本函数用于修改用户信息

    :接受信息: username(用户名) form(修改信息字典)

    :返回: Success code 0

    """
    user = User.objects.get(username=username)
    msg = STATUS_CODE['Success']
    del form['username']
    if 'gender' in form and not form['gender'] == '':
        if form['gender'] == '男':
            user.gender = 'male'
        else:
            user.gender = 'female'
        del form['gender']
    if 'password' in form and not form['password'] == '':
        if user.user_type is not USER_TYPE['customer']:
            user.set_password(form['password'])
        del form['password']
    for key in form.keys():
        if hasattr(user, key) and not form[key] == '':
            setattr(user, key, form[key])
    user.save()
    return msg


def get_or_create_default_seller():
    """
    本函数用于获取或创建默认的地推人员，该地推的价格为所有地推中的最高价

    :返回: QueryDict

    """
    if not SellerInfo.objects.all().order_by('-price'):
        price = 0.1
    else:
        price = SellerInfo.objects.all().order_by('-price').first().price
    if not price:
        price = 0.1
    default_seller = User.objects.get_or_create(
        username="defseller", password='defseller',
        user_type=USER_TYPE['seller'])[0]
    if not SellerInfo.objects.filter(seller=default_seller):
        seller = SellerInfo.objects.create(seller=default_seller, price=0)
    else:
        seller = SellerInfo.objects.filter(seller=default_seller).first()
    print(seller)
    price = SellerInfo.objects.all().order_by('-price').first().price
    if not price:
        seller.price = price
    else:
        seller.price = 0.1
    seller.save()
    return seller
