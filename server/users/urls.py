# -*- coding: utf-8 -*-

'''本文件用于配置'user/'下的 url '''


from django.urls import path

from .views import (get_qrcode, superuser_arrange_cc, superuser_get_cc,
                    superuser_view_newstu, superuser_viewlog)

urlpatterns = [
    path('qrcode', get_qrcode),
    path('superuser_viewlog', superuser_viewlog),
    path('superuser_view_newstu', superuser_view_newstu),
    path('superuser_get_cc', superuser_get_cc),
    path('superuser_arrange_cc', superuser_arrange_cc)
]
