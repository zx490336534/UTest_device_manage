from django.db import models
from utils.base_models import BaseModel

status_choice = ((0, '空闲'), (1, '使用中'))
sd_status_choice = ((0, '无'), (1, '有'))


class Device_info(BaseModel):
    id = models.AutoField(verbose_name='id主键', primary_key=True, help_text='id主键')
    device_ip = models.CharField('设备IP', max_length=200, unique=True, help_text='设备IP')
    device_name = models.CharField('设备名称', max_length=200, help_text='设备名称')
    device_version = models.CharField('设备版本', max_length=200, help_text='版本信息')
    tool_ip = models.CharField('工装设备IP', max_length=200, unique=True, help_text='工装设备IP')
    tool_pc_ip = models.CharField('工装电脑IP', max_length=200, help_text='工装电脑IP')
    daily_status = models.IntegerField('每日编译状态', choices=status_choice, default=0, help_text='每日编译状态')
    use_status = models.IntegerField('设备使用状态', choices=status_choice, default=0, help_text='设备使用状态')
    sd_status = models.IntegerField('SD卡状态', choices=sd_status_choice, default=0, help_text='SD卡状态')
    address = models.CharField('设备位置', max_length=200, null=True, blank=True, default='', help_text='设备位置')

    class Meta:
        db_table = 'u_device_info'
        verbose_name = '设备信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.device_ip}-{self.device_name}"
