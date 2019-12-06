import os
from datetime import datetime
from django.conf import settings
from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from . import serializers
from .models import Device_info


class DeviceViewSet(ModelViewSet):
    """
    list:
    返回(多个)设备信息

    create:
    添加设备信息

    retrieve:
    返回项目(单个)详情数据

    update:
    更新(全)设备信息

    partial_update:
    更新(部分)设备信息

    destroy:
    删除设备信息

    """
    queryset = Device_info.objects.filter(is_delete=False)
    serializer_class = serializers.DeviceModelSerializer
    ordering_fields = ('id', 'name')

    def perform_destroy(self, instance):
        instance.is_delete = True
        instance.save()  # 逻辑删除
