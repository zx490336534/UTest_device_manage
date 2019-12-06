# -*- coding:utf-8 -*-
"""
@Describe: urls
@Author: zhongxin
@Time: 2019-12-06 20:21
@File: urls.py
@Email: 490336534@qq.com
"""
from rest_framework import routers
from .views import DeviceViewSet

router = routers.DefaultRouter()
router.register(r'device_manage', DeviceViewSet)
urlpatterns = [

]
urlpatterns += router.urls