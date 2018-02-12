from django.db import models
from django_mysql.models import JSONField,Model
from users.models import UserProfile,privatearea

# Create your models here.
#场景
class scene(models.Model):
    name = models.CharField(max_length=100)

#分类
class  category(models.Model):
    name = models.CharField(max_length=200,null=False)
    isroot = models.BooleanField(default=False)
    isleaf = models.BooleanField(default=False)
    parent = models.ForeignKey("category",on_delete=models.CASCADE,null=True)
    isdelete = models.BooleanField(default=False)


#品牌的图片
def brand_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/brands_<id>/<filename>
    return 'images/brands/brands_{0}/{1}'.format(instance.name, filename)

class brands(models.Model):
    name = models.CharField(max_length=100,null=False)
    logo = models.ImageField(upload_to=brand_directory_path)
    isdelete = models.BooleanField(default=False)

#产品类
class product(models.Model):
    name = models.CharField(max_length=100,null=True),
    description = models.CharField(max_length=200,verbose_name="说明")
    createtime= models.DateTimeField(auto_now_add=True)
    updatetime = models.DateTimeField(auto_now=True)
    status = models.IntegerField(default=0)
    isdelete = models.BooleanField(default=False)
    categoryid = models.ForeignKey(category,on_delete=models.CASCADE,null=True)
    attibutes=JSONField()
    brand = models.ForeignKey(brands,on_delete=models.CASCADE,null=True)
    yijiandaifa = models.BooleanField(default=False)
    newup = models.BooleanField(default=False)
    #brandlogo 用brand字段关联显示
    belongs = models.ForeignKey(UserProfile,on_delete=models.CASCADE,null=True)
    inprivatearea = models.BooleanField(default=False)
    privatearea = models.ForeignKey(privatearea,on_delete=models.CASCADE,null=True)
    scene = models.ForeignKey(scene,on_delete=models.CASCADE,null=True)

#sku类
class productItem(models.Model):
    price=models.DecimalField(default=0,decimal_places=2,max_digits=2)
    attibutes = JSONField()
    status = models.IntegerField(default=0)
    onshell = models.BooleanField(default=False)
    favouredprice = models.DecimalField(default=0,decimal_places=2,max_digits=2)
    isdelete = models.BooleanField(default=False)


#产品的图片
def product_directory_path(instance,filename):
    return 'product_{0}/{1}'.format(instance.user.id,filename)

class productImage(models.Model):
    productimage = models.ImageField(upload_to=product_directory_path)
    type = models.IntegerField(default=0)
    productid = models.ForeignKey(product,on_delete=models.CASCADE,null=True)

#tags
class tags(models.Model):
    tagname = models.CharField(max_length=50,null=False)



