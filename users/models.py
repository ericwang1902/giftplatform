from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class UserProfile(AbstractUser):
    authStatus=models.BooleanField(default=False)#认证状态
    mobile = models.CharField(max_length=20)#电话号码
    gender = models.BooleanField(default=True)#1男，0女
    type = models.CharField(max_length=10,choices=(("supplier","供应商"),("giftcompany","礼品公司"),("service","客服"),("admin","系统管管理员")))
    privatearea = models.IntegerField(default=0)#私有域的外键id
    inprivatearea = models.BooleanField(default=False)#1开通了私有域，2没有开通私有域
    viplevel = models.IntegerField(default=0)#vip等级的外键
    servicestaff=models.IntegerField(default=0)#分配的客服的外键

    def __str__(self):
        return self.username