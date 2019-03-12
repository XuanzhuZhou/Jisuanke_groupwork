# -*- coding: utf-8 -*-

'''本文件用于配置 url'''

from django.urls import path

from .views import (customer_info, customer_login_code,
                    customer_login_password, refund, refund_cancel,
                    register, register_success, view_courses,
                    view_pay_records, view_sections)

urlpatterns = [
    path('register', register, name='register'),
    path('refund', refund, name='refund'),
    path('courses', view_courses, name='courses'),
    path('info', customer_info, name='info'),
    path('sections', view_sections, name='sections'),
    path('refund_cancel', refund_cancel, name="refund_cancel"),
    path('login_password', customer_login_password, name='login_password'),
    path('login_code', customer_login_code, name='login_code'),
    path('pay_records', view_pay_records, name='pay_records'),
    path('register_success', register_success, name='register_success'),
]
