from django.db import models
from apps.users.models import UserProfile


class Advertising(models.Model):
    """
    广告模型
    """
    title = models.CharField(max_length=100, null=False, ) # 广告标题
    link = models.CharField(max_length=300) # 广告链接
    image = models.ImageField() # 广告封面
    status = models.IntegerField(default=1, ) # 状态 0 已发布 1 草稿
    publisher = models.ForeignKey(UserProfile, on_delete=models.CASCADE) # 发布人员
    create_time = models.DateTimeField(auto_now_add=True,blank=False)
    is_deleted = models.BooleanField(default=False) # 删除标志位
    position = models.CharField(max_length=100) # 广告位位置

