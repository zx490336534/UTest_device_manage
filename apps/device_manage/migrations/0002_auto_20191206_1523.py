# Generated by Django 2.2.5 on 2019-12-06 15:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('device_manage', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device_info',
            name='tool_ip',
            field=models.CharField(blank=True, default='', help_text='工装设备IP', max_length=200, null=True, verbose_name='工装设备IP'),
        ),
        migrations.AlterField(
            model_name='device_info',
            name='tool_pc_ip',
            field=models.CharField(blank=True, default='', help_text='工装电脑IP', max_length=200, null=True, verbose_name='工装电脑IP'),
        ),
    ]
