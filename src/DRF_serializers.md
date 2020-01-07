---
layout: post
title: DRF 序列化反序列化
slug: Python_Django_REST_framework
date: 2019-12-31 17:23
status: publish
author: 酒后的阿bill
categories:
  - devops
tags:
  - Django
  - Python
  - DRF
excerpt: Django REST framework 序列化反序列化
---

# 1. 处理流程

## 1.1 反序列化(数据入库)：
在creat e方法中把关联数据单独拿出来，先正常处理其中一个模型的数据(如果是多对一关系，则需要先创建“一”这个模型的数据)， 再调用自定义的函数处理另一个模型的数据。

## 1.2 序列化(数据展示)：
在to_representation方法中先正常取出其中一个模型的数据，再将另一个模型的数据增加到已经查询出的数据中。

## 1.3 场景
需要将服务器相关的数据存入到数据库中并在前端展示。服务器包括实例ID、CPU、内存等唯一且必需的参数，也包括数据磁盘这一特 殊参数：

- 每台服务器的数据磁盘数量不固定，可能是0个(没有数据磁盘)，也可能是多个，但大部分服务器都是一个数据磁盘。

- 每一个数据磁盘都有磁盘ID、磁盘大小等参数。

原始数据：

- 三块数据磁盘
```json
('instanceId': 'ins-olfzusjv','instanceType': 'M2.MEDIUM16','cpu': 2, 'memory': 16, 'instanceName':'运维测试 1-公用'cre atedTime': '2019-11-14T04:57:06Z', 'expiredTime': '2020-05-14T04:57:11Z', 'bandwidthOut': 1, 'systemDiskID': 'disk-3u84a3q 5', 'systemDiskSize': 50, 'dataDisks': [('DiskSize': 200, 'DiskType': 'CLOUD_SSD', 'DiskId': 'disk-0sw362zd', 'DeleteWithI nstance': None), ('DiskSize': 110, 'DiskType': 'CLOUD_BASIC', 'DiskId': 'disk-nt2s8z11', 'DeleteWithInstance': None), ('Di skSize': 100, 'DiskType': 'CLOUD_BASIC', 'DiskId': 'disk-h00ds6mt', 'DeleteWithInstance': None)])
```

- 无数据盘
```json
('instanceId': 'ins-olfzusjv', 'instanceType': 'M2.MEDIUM16', 'cpu': 2, 'memory': 16, 'instanceName':'运维测试 1-公用'cre atedTime': '2019-11-14T04:57:06Z', 'expiredTime': '2020-05-14T04:57:11Z', 'bandwidthOut': 1, 'systemDiskID': 'disk-3u84a3q 5', 'systemDiskSize': 50, 'dataDisks': None)
```

- 使用两个模型存储数据：s ervers模型用于存储服务器的常规、普通参数对应的数据，datadisk模型用于存储数据磁盘的数据。

- 数据磁盘的数据在传入前进行处理，确保数据磁盘不存在时，它的值是一个空列表，而不是Non e或null。

- 通过调用API接口的方式，使用post方法手动传入数据。

# 2. code

## 2.1 创建模型

```python
from django.db import models

class Servers(models.Model):
	instanceld = models.CharField('服务器实例 ID', max_length=32, db_index=True, help_text='服务器实例 ID')
	instanceType = models.CharField('服务器实例类型’，max_length=32, help_text='服务器实例类型')
	cpu = models.CharField('CPU 核数',max_length=5, help_text='CPU', help_text='CPU 核数')
	memory = models.CharField('内存大小(GB)', max_length=10, help_text='内存大小(GB)')

class DataDisk(models.Model):
	server = models.ForeignKey(Servers,null=True)
	dataDiskID = models.CharField('系统磁盘容量’，max_length=32, help_text='系统磁盘容量')
	dataDiskSize = models.CharField('系统磁盘容量’，max_length=10, help_text='系统磁盘容量')
```

## 2.2 创建序列化类
```python
from rest_framework import serializers
from .models import Servers, DataDisk
#必须注意序列化时定义的字段和传入字段的一致性(名称、数据类型都要一致)，如果不一致则无法获取相关数据
class ServerSerializer(serializers.Serializer):
  id = serializers.ReadOnlyField()
  instanceId = serializers.CharField(required=True)
  cpu = serializers.CharField(required=True)
  memory = serializers.CharField(required=True)
  dataDisks = serializers.ListField(required=False, write_only=True)
  #to_internal_value是反序列化的第一步 #它将传入的diet的键值对转换成二元元组
  #如果需要对传入的原始数据进行增删改，则在这个函数中完成
  def to_internal_value(self, data):
    return super(ServerSerializer, self).to_internal_value(data)

  #字段级别的验证是在模型级别的验证之前进行的
  #字段级别的验证返回一个instance
  #如果需要对特定字段进行验证，则需要实现字段验证函数
  #字段验证函数的名称以’validate.'为前缀，后面跟上模型中定义的字段名。如:validate_dataDisks
  #字段级别的验证示例如下:
  #def validate_manufacturer(self, value):
  #  '''
  #  字段级别的验证。返回一个instance 验证制造商记录是否存在，如果不存在则创建并返回一个instance，如果存在则直接返回一个instance
  #  '''
  #  try:
  #   return Manufacturer.objects.get(vendor_name_exact=value)
  # except Manufacturer.DoesNotExist:
  #   return self.create_manufacturer(value)
  
  #validate方法是模型级别的验证
  #只有经过模型验证后的数据才会被传给create、update方法
  #模型级别的验证示例如下:
  # def validate(self, attrs):
  #   '''
  #   对象级别的验证。验证服务器型号。先拿到制造商的instance,然后查找该制造商对应的记录是否存在该型号
  #   '''
  #   manufacturer_obj = attrs["manufacturer"] 
  #   try:
  #     attrs["model_name"] = manufacturer_obj.productmodel_set.get(model_name_exact=attrs["model_name"]) 
  #     except 
  #     ProductModel.DoesNotExist:
  #     attrs["model_name"] = self.create_product_model(manufacturer_obj, attrs["model_name"])
  #   return attrs
  #新增数据和更新数据的操作大同小异，区别在于传入到函数的参数中是否包含instance 
  #如果有instance，则是数据更新，否则就是新增数据

  #create方法接收验证后的数据，并将数据保存到数据库中
  #如果涉及到模型的关联关系，即数据要存入到多张表中，则按下面的思路操作:
  #将关联表的数据单独从validated_data中提取出来，并传入自定义的函数中，通过该自定义函数完成关联模型数据的写入
  #示例如下:
  def create(self, validated_data):
    instanceId = validated_data["instanceId"]
    instance = self.getlnstance(instanceId)
    dataDisks = validated_data.pop("dataDisks")
      # print(dataDisks)
      if instance is not None:
        self.check_data_disk(instance, dataDisks)
        return self.update(instance, validated_data)
      else:
        instance = Servers.objects.create(**validated_data)
        self.check_data_disk(instance, dataDisks)
        return instance
  # update方法接收instance和validated_data，将指定的字段数据更新写入到数据库中
  
  #如果涉及模型的关联关系，则需要调用自定义的函数来实现关联表的更新操作
  def update(self, instance, validated_data):
    instance.cpu = validated_data.get("cpu","")
    instance.memory = validated_data.get("memory","")
    instance.save()
    return instance

  #获取服务器实例
  def getInstance(self, instanceId):
    try:
      return Servers.objects.get(instanceId_exact=instanceId)
    except Servers.DoesNotExist:
      return None
    except Exception as e:
      raise serializers.ValidationError("服务器错误:{)".format(e))

  #对关联模型操作的自定义函数
  #该函数实现了对磁盘信息的增、删、改
  def check_data_disk(self, instance, dataDisks):
    data_disk_queryset = instance.datadisk_set.all()
    current_data_disk =[]
    for datadisk in dataDisks:
      try:
        data_disk_obj = data_disk_queryset.get(dataDiskID_exact=datadisk['DiskId'])
      except DataDisk.DoesNotExist:
        data_disk_obj = DataDisk.objects.create(dataDiskID=datadisk['DiskId'], dataDiskSize=datadisk['DiskSize'],server=instance)
          current_data_disk.append(data_disk_obj)

    self.cleanDisk(data_disk_queryset, current_data_disk)

  #自定义函数，用于删除多余的磁盘记录
  def cleanDisk(self, data_disk_queryset, current_data_disk):
    not_exists_disk = set(data_disk_queryset) - set(current_data_disk)
    for obj in not_exists_disk:
      obj.delete()

  # to_representation函数是序列化的最后一步，如果需要对序列化的数据进行增删改，则在该函数中实现
  #由于涉及模型关联，所以需要对返回给前 端的数据进行处理
  #通过模型关系取出数据磁盘的相关数据，并增加到需要返回给前端的数据中
  def to_representation(self, instance):
    ret = super(ServerSerializer, self).to_representation(instance)
    disks = instance.datadisk_set.all().values()
    disks_list =[]
    for i in disks:
      disks_list.append(i)
    ret["dataDisks"] = disks_list
    return ret
```

## 2.3 创建视图

```python
from rest_framework import viewsets
from .serializers import ServerSerializer
from .models import Servers
class ServerViewset(viewsets.ModelViewSet):
	queryset = Servers.objects.all()
	serializer_class = ServerSerializer
```

## 2.4 URL
```python
from server.views import ServerViewset
route.register('servers',ServerViewset,base_name='servers')

urlpatterns = [
    url(r'^', include(route.urls)),
  ]
```
