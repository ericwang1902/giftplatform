from django.db import models


class Invitation(models.Model):
    """
    邀请试用
    """
    # 公司名称
    company_name = models.CharField(max_length=50, null=True, blank=True)

    # 姓名
    name = models.CharField(max_length=50, null=True, blank=True)

    # 职位
    job_position = models.CharField(max_length=50, null=True, blank=True)

    # 电话
    tel = models.CharField(max_length=50, null=True, blank=True)

    # Email
    email = models.EmailField(null=True, blank=True)

    # 是否已读
    has_read = models.BooleanField(default=False)

    # 创建时间
    created_at = models.DateTimeField(auto_now_add=True)

    # 是否已经删除
    is_delete = models.BooleanField(default=False)
