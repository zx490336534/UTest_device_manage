# 自动化设备管理平台

## 需求

1. 设备信息添加
- 设备IP
- 设备名称
- 设备版本
- 工装设备IP
- 工装电脑IP
- 每日编译状态「只读」
> TODO:修改时间大于x天自动释放

- 设备使用状态「只读」
- 设备SD卡状态
- 设备位置
- 添加时间
- 修改时间「不可见」
- 逻辑删除「不可见」
2. 获取空闲设备

- 输入`设备IP`返回使用状态

```json
{'device_ip': '203.1.4.10'}
```

- 输入`设备名称`返回使用状态

```json
data = {'device_name': 'abc'}
```

- 输入`测试类型`「每日编译/正式版本/工装」返回空闲设备列表

```json
data = {'type': 'daily'}
data = {'type': 'tool'}
data = {'type': 'unuse'}
```

3. 修改使用状态
- 使用`设备IP`+`使用状态`来进行修改

```json
{
    'device_ip': '203.1.4.10',
    'use_status': 0,
    'daily_status': 0
}
```

## 数据库设计

设备ip`device_ip`唯一

```python
from django.db import models
from utils.base_models import BaseModel

status_choice = ((0, '空闲'), (1, '使用中'))
sd_status_choice = ((0, '无'), (1, '有'))


class Device_info(BaseModel):
    id = models.AutoField(verbose_name='id主键', primary_key=True, help_text='id主键')
    device_ip = models.CharField('设备IP', max_length=200, unique=True, help_text='设备IP')
    device_name = models.CharField('设备名称', max_length=200, help_text='设备名称')
    device_version = models.CharField('设备版本', max_length=200, help_text='版本信息')
    tool_ip = models.CharField('工装设备IP', max_length=200, null=True, blank=True, default='', help_text='工装设备IP')
    tool_pc_ip = models.CharField('工装电脑IP', max_length=200, null=True, blank=True, default='', help_text='工装电脑IP')
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
```



## 获取空闲设备

使用`request.data`从post请求中拿到数据

```python
data = request.data
device_ip = data.get('device_ip')
device_name = data.get('device_name')
type = data.get('type')
```

### 情况1:根据设备IP

由于`device_ip`唯一，直接返回找到的设备信息

```python
device_info_objs = self.queryset.filter(device_ip=device_ip).first()
```

### 情况2:根据设备名称

返回全部该设备名称的内容

```python
device_info_objs = self.queryset.filter(device_name=device_name).all()
```

### 情况3:根据类型

#### 每日编译

`daily_status`和`use_status`都为0的第一个内容

```python
device_info_objs = self.queryset.filter(daily_status=0, use_status=0).first()
```

#### 工装

获取`use_status=1`的工装电脑ip列表

```python
working = self.queryset.values('tool_pc_ip').annotate(use=Count('use_status')).filter(
                    use_status=1).filter(tool_pc_ip__contains='.').all()
working_list = list(working)
```

挑选出不包含上述工装电脑IP的设备

```python
if working_list:
  print([f"跳过的工装PC:{i.get('tool_pc_ip')}" for i in working_list])
  device_info_objs = self.queryset.filter(~Q(tool_pc_ip=working_list[0].get('tool_pc_ip')))
  device_info_objs = device_info_objs.filter(tool_pc_ip__contains='.')
  for i in working_list[1:]:
    a = ~Q(tool_pc_ip=i.get('tool_pc_ip'))
    device_info_objs = device_info_objs.filter(a)
```

#### 普通未使用设备

`use_status=0`且不是工装的设备

```python
device_info_objs = self.queryset.filter(is_delete=False,use_status=0).filter(tool_pc_ip='').filter(tool_ip='').all()
```

### 全部代码

```python
@action(methods=['post'], detail=False)
def status(self, request):
    """
    获取设备状态
    {
        "device_ip":"",
        "device_name":"",
        "type":"daily/tool/unuse"
    }
    """
    data = request.data
    device_ip = data.get('device_ip')
    device_name = data.get('device_name')
    type = data.get('type')
    device_info_objs = self.queryset
    if device_ip:
        # 根据设备IP查找,返回一个
        device_info_objs = self.queryset.filter(device_ip=device_ip).first()
    elif device_name:
        # 根据设备名称查找,返回全部
        device_info_objs = self.queryset.filter(device_name=device_name).all()
    elif type:
        if type == 'daily':
            # 每日编译状态为0 且设备使用状态为0,返回一个
            device_info_objs = self.queryset.filter(daily_status=0, use_status=0).first()
        elif type == 'tool':
            # 有工装IP 同一工装电脑下设备使用状态为0,返回全部
            # 查找 tool_pc_ip有「.」内容且 use_status为1的全部电脑IP
            working = self.queryset.values('tool_pc_ip').annotate(use=Count('use_status')).filter(
                use_status=1).filter(tool_pc_ip__contains='.').all()
            working_list = list(working)
            if working_list:
                print([f"跳过的工装PC:{i.get('tool_pc_ip')}" for i in working_list])
                device_info_objs = self.queryset.filter(~Q(tool_pc_ip=working_list[0].get('tool_pc_ip')))
                device_info_objs = device_info_objs.filter(tool_pc_ip__contains='.')
                for i in working_list[1:]:
                    a = ~Q(tool_pc_ip=i.get('tool_pc_ip'))
                    device_info_objs = device_info_objs.filter(a)
            else:
                return Response({'status': -1, 'error': '没有空闲的工装设备'})
        elif type == 'unuse':
            # 任意非使用状态的普通设备,返回全部
            device_info_objs = self.queryset.filter(is_delete=False, use_status=0).filter(tool_pc_ip='').filter(
                tool_ip='').all()
    else:
        return Response({'status': -1, 'error': '请使用正确的查询方式'})
    if device_ip or type == 'daily':
        serializer = self.get_serializer(device_info_objs, many=False)
    else:
        serializer = self.get_serializer(device_info_objs, many=True)
    new_data = get_count_by_device_info(serializer.data)
    return Response(new_data)
```

## 修改设备状态

从数据库中检索`device_ip=device_ip`的内容

```python
device_info = self.queryset.filter(device_ip=device_ip).first()
device_info.use_status = use_status
device_info.daily_status = daily_status
```

```python
@action(methods=['post'], detail=False)
def use(self, request, *args, **kwargs):
   """
   修改设备使用状态
        {
            "device_ip":'',
            "use_status":0或1,
            "daily_status":0或1
        }
    """
    data = request.data
    device_ip = data.get('device_ip')
    use_status = data.get('use_status')
    daily_status = data.get('daily_status')
    device_info = self.queryset.filter(device_ip=device_ip).first()
    if use_status in [0, 1] and daily_status in [0, 1] and device_info:
      device_info.use_status = use_status
      device_info.save()
      serializer = serializers.DeviceModelSerializer(instance=device_info)
      return Response(serializer.data)
    else:
      return Response({'status': -1, 'error': 'use_status和daily_status只能为0或1'})
```

## 部署

在`Deploydevice_manage`路径下

```shell
$ docker-compose up
```

![image-20191207130334825](https://tva1.sinaimg.cn/large/006tNbRwly1g9o2qbxb2lj31b30u0qm7.jpg)