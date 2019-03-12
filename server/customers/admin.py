# -*- coding: utf-8 -*-

'''本文件用于将 model 显示在 admin 页面'''
from django.contrib import admin

from .models import Customer

# Register your models here.
admin.site.register(Customer)
