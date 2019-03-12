# -*- coding: utf-8 -*-

'''本文件用于构建和课程紧密相关的数据库表'''

from django.db import models


class Teacher(models.Model):
    '''该表用来存储上课教师的信息'''
    name = models.CharField(max_length=20, blank=False)
    tel = models.CharField(max_length=11, blank=True, null=True)


def get_teacher():
    '''返回一个标记为已删除的 Teacher 行'''
    return Teacher.objects.get_or_create(name='deleted')[0]


class Courses(models.Model):
    '''该表用来存储课程信息'''
    DATE_CHOICES = (
        (1, '星期一'),
        (2, '星期二'),
        (3, '星期三'),
        (4, '星期四'),
        (5, '星期五'),
        (6, '星期六'),
        (7, '星期七'),
    )

    name = models.CharField(max_length=20, blank=False)
    teacher_id = models.ForeignKey(
        Teacher,
        related_name='teacher',
        on_delete=models.SET(get_teacher)
    )
    time = models.TimeField(blank=True, null=True)
    date = models.PositiveSmallIntegerField(
        choices=DATE_CHOICES, default=0)
    time_length = models.PositiveIntegerField(default=120)
    total_sec = models.PositiveIntegerField(default=0)
    price = models.FloatField(null=True, blank=True)


class Section(models.Model):
    '''该表用来存储课节'''
    course_id = models.ForeignKey(
        Courses,
        related_name='sections',
        on_delete=models.CASCADE
    )
    count = models.PositiveIntegerField()
    name = models.CharField(max_length=30, blank=True, null=True)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    location = models.CharField(max_length=100)
    is_cancel = models.BooleanField(default=False)
