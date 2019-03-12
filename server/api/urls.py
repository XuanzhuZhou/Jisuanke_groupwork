# -*- coding: utf-8 -*-

'''本文件用于配置url'''

from django.urls import path

from .views import (login, logout, change_password,
                    recieve_message_request,
                    check_login, get_sellrecords,
                    deal_register_pay,
                    class_pay, cc_view_customers,
                    eduadmin_get_courses,
                    eduadmin_cancell_courses,
                    eduadmin_ensure_cancell,
                    eduadmin_arrange_course,
                    eduadmin_check_refund,
                    eduadmin_ensure_refund,
                    cc_check_refund, cc_ensure_refund,
                    view_ccrecords, cc_signup_info,
                    superuser_register, superuser_import_customer,
                    superuser_modify_customer, superuser_modify_user,
                    superuser_view_users, superuser_view_customers,
                    superuser_delete_customer, superuser_delete_user)


urlpatterns = [
    path('login', login),
    path('logout', logout),
    path('change_password', change_password),
    path('sendmsg', recieve_message_request),
    path('payviews', deal_register_pay),
    path('payclass', class_pay),
    path('get_sellrecords', get_sellrecords),
    path('eduadmin_get_courses', eduadmin_get_courses),
    path('eduadmin_cancell_courses', eduadmin_cancell_courses),
    path('eduadmin_ensure_cancell', eduadmin_ensure_cancell),
    path('eduadmin_arrange_course', eduadmin_arrange_course),
    path('eduadmin_check_refund', eduadmin_check_refund),
    path('eduadmin_ensure_refund', eduadmin_ensure_refund),
    path('cc_check_refund', cc_check_refund),
    path('cc_ensure_refund', cc_ensure_refund),
    path('check_login', check_login),
    path('view_ccrecords', view_ccrecords),
    path('cc_signup_info', cc_signup_info),
    path('superuser_register', superuser_register),
    path('sup_import_customer', superuser_import_customer),
    path('modify_customer', superuser_modify_customer),
    path('modify_user', superuser_modify_user),
    path('sup_view_users', superuser_view_users),
    path('sup_view_customers', superuser_view_customers),
    path('delete_user', superuser_delete_user),
    path('delete_customer', superuser_delete_customer),
    path('cc_view_customers', cc_view_customers)
]
