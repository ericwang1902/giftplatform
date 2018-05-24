from django.db import models
from django.contrib.auth.models import AbstractUser
from apps.viplevels.models import vipLevel


# Create your models here.

# 私有域配置
class privatearea(models.Model):
    accountlimit = models.IntegerField(default=0)
    productlimit = models.IntegerField(default=0)
    status = models.IntegerField(default=0) # 私有域状态 0 启用 1 关闭


class UserProfile(AbstractUser):
    authStatus = models.BooleanField(default=False)  # 认证状态
    currentpoint = models.CharField(max_length=100, null=True, choices=(("ck", "等待管理员审核"), ("bc", "被退回")))  # 表示当前审核所在节点
    mobile = models.CharField(max_length=20, null=True)  # 电话号码
    gender = models.BooleanField(default=True)  # 1男，0女
    type = models.CharField(max_length=100, null=True, choices=(
        ("supplier", "供应商"), ("giftcompany", "礼品公司"), ("service", "客服"), ("admin", "系统管管理员")))
    privatearea = models.ForeignKey(privatearea, on_delete=models.CASCADE, blank=True, null=True)  # 私有域的外键id
    inprivatearea = models.BooleanField(default=False)  # 1开通了私有域，2没有开通私有域
    viplevel = models.ForeignKey(vipLevel, on_delete=models.CASCADE, blank=True, null=True)  # vip等级的外键
    servicestaff = models.ForeignKey("UserProfile", on_delete=models.CASCADE, blank=True, null=True)  # 分配的客服的外键

    def __str__(self):
        return self.username


def user_directory_path(instance, filename):
    return 'images/authinfo/{0}/{1}'.format(instance.userid, filename)


# 认证图片
class userAuthinfo(models.Model):
    img = models.ImageField(upload_to=user_directory_path)
    userid = models.ForeignKey(UserProfile, on_delete=models.CASCADE)


# viplevel变更历史
class vipLevelChangeHistory(models.Model):
    updatetime = models.DateTimeField(auto_now_add=True)  # 更新时间
    start_time = models.DateTimeField(null=True) # 会员开始时间
    end_time = models.DateTimeField(null=True) # 会员结束时间
    userid = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    orignallevel = models.ForeignKey(vipLevel, related_name="orignallevel", on_delete=models.CASCADE, null=True, blank=True)  # 原状态
    destlevel = models.ForeignKey(vipLevel, related_name="destlevel", on_delete=models.CASCADE)  # 目标状态


# 站内信
class siteMessge(models.Model):
    fromuser = models.ForeignKey(UserProfile, related_name="fromuser", on_delete=models.CASCADE)
    touser = models.ForeignKey(UserProfile, related_name="touser", on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=500, null=True)
    content = models.CharField(max_length=500, null=True)
    isdelete = models.BooleanField(default=False)
    hasread = models.BooleanField(default=False)
    publishdate = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    updatetime = models.DateTimeField(auto_now=True,null=True, blank=True)
    status = models.CharField(max_length=100, choices=(("pass", "审核通过"), ("waitting", "等待审核"), ("reject", "审核驳回")), default="waitting") # 站内公告的审核状态


def wechat_qr_path(instance, filename):
    """
    微信二维码图片
    :param instance:
    :param filename:
    :return:
    """
    ext = filename.split('.')[-1]
    return 'images/suppliers/{0}/{1}_wechat_qr_code.{2}'.format(instance.userid.id, instance.userid.id, ext)


# supplier的补充数据结构
class supplier(models.Model):
    suppliername = models.CharField(max_length=200, null=False)
    tel = models.CharField(max_length=20, null=False)
    qq = models.CharField(max_length=20, null=True, blank=True)
    email = models.CharField(max_length=40, null=False)
    userid = models.OneToOneField(UserProfile, on_delete=models.CASCADE, blank=True, null=True)
    wechat_qr_code_img = models.ImageField(upload_to=wechat_qr_path, blank=True, null=True)
