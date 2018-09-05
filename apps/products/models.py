from django.db import models
from django_mysql.models import JSONField,Model
from apps.users.models import UserProfile,privatearea
import uuid, datetime

# Create your models here.
#场景
class scene(models.Model):
    name = models.CharField(max_length=100)

#分类
class  category(models.Model):
    name = models.CharField(max_length=200,null=False)
    isroot = models.BooleanField(default=False)
    isleaf = models.BooleanField(default=False)
    parent = models.ForeignKey("category",on_delete=models.CASCADE,blank=True,null=True)
    isdelete = models.BooleanField(default=False)


#品牌的图片
def brand_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/brands_<id>/<filename>
    return 'images/brands/brands_{0}/{1}'.format(instance.name, filename)

class brands(models.Model):
    name = models.CharField(max_length=100,null=False)
    logo = models.ImageField(upload_to=brand_directory_path)
    isdelete = models.BooleanField(default=False)

#tags
class tags(models.Model):
    tagname = models.CharField(max_length=50,null=False)

#产品类
class product(models.Model):
    name = models.CharField(max_length=100,null=True)
    model = models.CharField(max_length=100, verbose_name="型号", null=True, blank=True)
    description = models.TextField(verbose_name="说明",null=True,blank=True)
    simple_description = models.TextField(verbose_name="卖点", null=True,blank=True)
    createtime= models.DateTimeField(auto_now_add=True)
    updatetime = models.DateTimeField(auto_now=True)
    status = models.IntegerField(default=0)
    isdelete = models.BooleanField(default=False)
    categoryid = models.ForeignKey(category,on_delete=models.CASCADE,blank=True,null=True)
    attributes=JSONField()
    brand = models.ForeignKey(brands,on_delete=models.CASCADE,null=True)
    yijiandaifa = models.BooleanField(default=False)
    newup = models.BooleanField(default=False)
    #brandlogo 用brand字段关联显示
    belongs = models.ForeignKey(UserProfile,on_delete=models.CASCADE,null=True)
    inprivatearea = models.BooleanField(default=False)
    privatearea = models.ForeignKey(privatearea,on_delete=models.CASCADE,blank=True,null=True)
    scenes = models.ManyToManyField(tags)

#sku类
class productItem(models.Model):
    price=models.DecimalField(default=0,decimal_places=2,max_digits=10)
    attributes = JSONField()
    status = models.IntegerField(default=0)
    onshell = models.BooleanField(default=False)
    favouredprice = models.DecimalField(default=0,decimal_places=2,max_digits=10)
    stock = models.IntegerField(default=0, blank=True, null=True)
    isdelete = models.BooleanField(default=False)
    product = models.ForeignKey(product, related_name='productItems', on_delete=models.CASCADE, blank=True,null=True)


#产品的图片
def product_directory_path(instance,filename):
    filename = '%s_%s' % (uuid.uuid4(),filename)
    return 'product_{0}/{1}'.format(datetime.date.today().strftime("%Y%m%d"),filename)

class productImage(models.Model):
    productimage = models.ImageField(upload_to=product_directory_path)
    type = models.IntegerField(default=0) # 0 主图 1 规格图
    productid = models.ForeignKey(product,on_delete=models.CASCADE,null=True, related_name='images')
    product_item_id = models.ForeignKey(productItem, on_delete=models.CASCADE,null=True,related_name='images')



