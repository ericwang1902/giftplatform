from django.db import models

# Create your models here.

#vip功能
class vipFunction(models.Model):
    functionname = models.CharField(max_length=100,null=True)


#vip等级
class  vipLevel(models.Model):
    vipname=models.CharField(max_length=100,null=True,verbose_name="vip等级名称")
    description = models.CharField(max_length=300,null=True,verbose_name="vip等级说明")
    vipFunctions = models.ManyToManyField(
        vipFunction,
        through='levelToFunction',
        through_fields=('viplevelid','vipfunctionid')
    )
    class Meta:
        verbose_name = "vip等级"
        verbose_name_plural = verbose_name

#vip等级和功能关联表
class levelToFunction(models.Model):
    viplevelid = models.ForeignKey(vipLevel,on_delete=models.CASCADE)
    vipfunctionid = models.ForeignKey(vipFunction,on_delete=models.CASCADE)



