import os
from datetime import datetime
from django.conf import settings
from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from device_manage.utils import get_count_by_device_info
from utils.timeoperator import change_time
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
    ordering_fields = ('id', 'device_ip')

    def perform_destroy(self, instance):
        instance.is_delete = True
        instance.save()  # 逻辑删除

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        response.data['results'] = get_count_by_device_info(response.data['results'])
        return response

    @action(methods=['post'], detail=False)
    def status(self, request):
        """
        获取设备状态
        """
        data = request.data
        device_ip = data.get('device_ip')
        device_name = data.get('device_name')
        type = data.get('type')
        device_info_objs = self.queryset
        if device_ip:
            # 根据设备IP查找,返回一个
            device_info_objs = Device_info.objects.filter(is_delete=False, device_ip=device_ip).first()
        elif device_name:
            # 根据设备名称查找,返回全部
            device_info_objs = Device_info.objects.filter(is_delete=False, device_name=device_name).all()
        elif type:
            if type == 'daily':
                # 每日编译状态为0 且设备使用状态为0,返回一个
                device_info_objs = Device_info.objects.filter(is_delete=False, daily_status=0, use_status=0).first()
            elif type == 'tool':
                # 有工装IP 同一工装电脑下设备使用状态为0,返回全部
                device_info_objs = Device_info.objects.filter(is_delete=False,
                                                              tool_ip__isnull=False,
                                                              use_status=0).all()
            elif type == 'unuse':
                # 任意非使用状态的设备,返回全部
                device_info_objs = Device_info.objects.filter(is_delete=False, use_status=0).all()
        else:
            return Response({'error': '请使用正确的查询方式'})
        serializer = self.get_serializer(device_info_objs, many=False)
        new_data = serializer.data
        new_data['create_time'] = change_time(new_data['create_time'])
        return Response(new_data)
