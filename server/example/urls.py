# -*- coding: utf-8 -*-

'''本文件用于配置 url '''


from django.urls import path

from .views import (response_get_method,
                    response_post_method_with_csrf_check,
                    response_post_method_without_csrf_check)


urlpatterns = [
    path('get', response_get_method),
    path('post', response_post_method_with_csrf_check),
    path('post_no_csrf', response_post_method_without_csrf_check)
]
