# -*- coding:utf-8 -*-
"""
@Describe: serializers
@Author: zhongxin
@Time: 2019-12-06 20:23
@File: serializers.py
@Email: 490336534@qq.com
"""
from rest_framework import serializers

from .models import Device_info


class DeviceModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device_info
        exclude = ('update_time', 'is_delete')

        extra_kwargs = {
            'create_time': {
                'read_only': True
            },
            'daily_status': {
                'read_only': True
            },
            'use_status': {
                'read_only': True
            },
            'tool_ip': {
                'allow_null': True
            },
            'tool_pc_ip': {
                'allow_null': True
            },

        }


class ChangeUseModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device_info
        fields = ('device_ip', 'use_status')
