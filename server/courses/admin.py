# -*- coding: utf-8 -*-

'''本文件用于将 model 显示在 admin 页面'''

from django.contrib import admin

from .models import Courses, Section, Teacher


class TeacherAdmin(admin.ModelAdmin):
    '''该类用来展示 Teacher 相关信息'''
    list_display = ['id', 'name', 'tel']


admin.site.register(Teacher, TeacherAdmin)


class CoursesAdmin(admin.ModelAdmin):
    '''该类用来展示 Courses 相关信息'''
    list_display = ['id', 'name', 'teacher_id', 'total_sec']


admin.site.register(Courses, CoursesAdmin)


class SectionAdmin(admin.ModelAdmin):
    '''该类用来展示 Courses 相关信息'''
    list_display = [
        'id', 'course_id', 'count', 'date',
        'name', 'start_time', 'end_time', 'location'
    ]


admin.site.register(Section, SectionAdmin)
