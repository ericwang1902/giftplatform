from django.db import models
from django.contrib.auth.models import AbstractUser
from viplevels.models import vipLevel
# Create your models here.

#私有域配置
class privatearea(models.Model):
    accountlimit = models.IntegerField(default=0)
    productlimit = models.IntegerField(default=0)



class UserProfile(AbstractUser):
    authStatus=models.BooleanField(default=False)#认证状态
    mobile = models.CharField(max_length=20)#电话号码
    gender = models.BooleanField(default=True)#1男，0女
    type = models.CharField(max_length=10,choices=(("supplier","供应商"),("giftcompany","礼品公司"),("service","客服"),("admin","系统管管理员")))
    privatearea = models.ForeignKey(privatearea,on_delete=models.CASCADE, blank=True, null=True)#私有域的外键id
    inprivatearea = models.BooleanField(default=False)#1开通了私有域，2没有开通私有域
    viplevel = models.ForeignKey(vipLevel,on_delete=models.CASCADE, blank=True, null=True)#vip等级的外键
    servicestaff=models.ForeignKey("UserProfile",on_delete=models.CASCADE, blank=True, null=True)#分配的客服的外键

    def __str__(self):
        return self.username


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.user.id, filename)


#认证图片
class userAuthinfo(models.Model):
    imgurl = models.ImageField(upload_to=user_directory_path)
    userid = models.ForeignKey(UserProfile,on_delete=models.CASCADE)


#viplevel变更历史
class vipLevelChangeHistory(models.Model):
    updatetime = models.DateTimeField(auto_now_add=True)#更新时间
    userid = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    orignallevel = models.ForeignKey(vipLevel,related_name="orignallevel",on_delete=models.CASCADE)#原状态
    destlevel = models.ForeignKey(vipLevel,related_name="destlevel", on_delete=models.CASCADE)#目标状态

#站内信
class siteMessge(models.Model):
    fromuser = models.ForeignKey(UserProfile,related_name="fromuser", on_delete=models.CASCADE)
    touser = models.ForeignKey(UserProfile,related_name="touser", on_delete=models.CASCADE)
    title = models.CharField(max_length=500,null=True)
    content = models.CharField(max_length=500,null=True)
    isdelete = models.BooleanField(default=False)
    hasread = models.BooleanField(default=False)

#supplier的补充数据结构
class supplier(models.Model):
    suppliername = models.CharField(max_length=200,null=False)
    tel  = models.CharField(max_length=20,null=False)
    qq = models.CharField(max_length=20,null=False)
    email = models.CharField(max_length=40,null=False)
    userid = models.ForeignKey(UserProfile,on_delete=models.CASCADE)