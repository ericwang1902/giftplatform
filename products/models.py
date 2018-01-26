from django.db import models

# Create your models here.
#场景
class scene(models.Model):
    name = models.CharField(max_length=100)

#分类
class  category(models.Model):
    name = models.CharField(max_length=200,null=False)
    isroot = models.BooleanField(default=False)
    isleaf = models.BooleanField(default=False)
    parent = models.ForeignKey("category",on_delete=models.CASCADE)
    isdelete = models.BooleanField(default=False)


#品牌的图片
def brand_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/brands_<id>/<filename>
    return 'brands_{0}/{1}'.format(instance.user.id, filename)

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
    categoryid = models.ForeignKey(category,on_delete=models.CASCADE)
    #attibutes=json

#sku类
class productItem(models.Model):
    price=models.DecimalField(default=0)
    #attributes = json
    status = models.IntegerField(default=0)
    onshell = models.BooleanField(default=False)
    favouredprice = models.DecimalField(default=0)
    isdelete = models.BooleanField(default=False)


#产品的图片
def product_directory_path(instance,filename):
    return 'product_{0}/{1}'.format(instance.user.id,filename)

class productImage(models.Model):
    productimage = models.ImageField(upload_to=product_directory_path)
    type = models.IntegerField(default=0)
    productid = models.ForeignKey(product,on_delete=models.CASCADE)



