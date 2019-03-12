# -*- coding: utf-8 -*-

'''本文件用于配置url'''

from django.urls import path

from .views import (add_section, change_course_info,
                    change_section_info, edu_courses_info, add_new_course)

urlpatterns = [
    path('edu_courses_info', edu_courses_info),
    path('change_course_info', change_course_info),
    path('change_section_info', change_section_info),
    path('add_section', add_section),
    path('add_new_course', add_new_course)
]
