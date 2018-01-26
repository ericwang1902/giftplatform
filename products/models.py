from django.db import models

# Create your models here.

class  category(models.Model):
    name = models.CharField(max_length=200,null=False)
    isroot = models.BooleanField(default=False)
    isleaf = models.BooleanField(default=False)
    parent = models.ForeignKey("category",on_delete=models.CASCADE)
    isdelete = models.BooleanField(default=False)


class product(models.Model):
    name = models.CharField(max_length=100,null=True),
    description = models.CharField(max_length=200,verbose_name="说明")
    createtime= models.DateTimeField(auto_now_add=True)
    updatetime = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=False)
    isdelete = models.BooleanField(default=False)
    categoryid = models.ForeignKey(category,on_delete=models.CASCADE)
    #attibutes=json
