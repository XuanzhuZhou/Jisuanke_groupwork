# -*- coding: utf-8 -*-

'''本文件用于配置url'''

from django.urls import path

from .views import (today_grades, today_seller_grades, today_cc_grades,
                    week_seller_grades, week_cc_grades, months_seller_grades,
                    years_seller_grades, years_cc_grades,
                    get_seller_distribution, audition_grades,
                    superuser_import_courses, months_cc_grades,
                    create_audition_records)

urlpatterns = [
    path('today_grades', today_grades),
    path('today_seller_grades', today_seller_grades),
    path('week_seller_grades', week_seller_grades),
    path('months_seller_grades', months_seller_grades),
    path('years_seller_grades', years_seller_grades),
    path('today_cc_grades', today_cc_grades),
    path('week_cc_grades', week_cc_grades),
    path('months_cc_grades', months_cc_grades),
    path('years_cc_grades', years_cc_grades),
    path('get_seller_distribution', get_seller_distribution),
    path('audition_grades', audition_grades),
    path('import_courses', superuser_import_courses),
    path('create_audition_records', create_audition_records)
]
