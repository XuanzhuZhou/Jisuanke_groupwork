# -*- coding: utf-8 -*-

'''本文件用于将 model 显示在 admin 页面'''

from django.contrib import admin

from .models import (AuditionRecord, CcRecord, OperationLogs,
                     OtherResource, RefundRecord, SellRecord)

# Register your models here.
admin.site.register(OtherResource)
admin.site.register(AuditionRecord)
admin.site.register(CcRecord)
admin.site.register(SellRecord)
admin.site.register(RefundRecord)
admin.site.register(OperationLogs)
