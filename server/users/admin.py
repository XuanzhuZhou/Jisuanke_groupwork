# -*- coding: utf-8 -*-

'''本文件用于建立后台注册模型'''

from django.contrib import admin

from .models import SellerInfo, User

# Register your models here.

admin.site.register(User)
admin.site.register(SellerInfo)
