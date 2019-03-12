# -*- coding: utf-8 -*-


'''本文件用于在 admin 界面展示数据库表'''

from django.contrib import admin
from .models import VerifyCode

admin.site.register(VerifyCode)
