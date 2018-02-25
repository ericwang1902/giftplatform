# _*_ coding:utf-8 _*_

__author__ = 'ericwang'
__date__ = '2018/2/2 18:41'

from products.models import brands,category,product,tags,productItem,productImage
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from datetime import datetime
from django.db.models import Q
import json


class brandSerializer(ModelSerializer):
    class Meta:
        model = brands
        fields = "__all__"

class categorySerializer(ModelSerializer):
    class Meta:
        model = category
        fields = "__all__"

class ProductImageUploaderSerializer(ModelSerializer):
    class Meta:
        model = productImage
        fields = "__all__"

class ProductItemSerializer(ModelSerializer):
    images = serializers.ListField(
        child=serializers.IntegerField()
    )
    class Meta:
        model = productItem
        fields = "__all__"

class ProductSerializer(ModelSerializer):
    productItems = ProductItemSerializer(many=True)
    images = serializers.ListField(
        child=serializers.IntegerField()
    )

    class Meta:
        model = product
        fields = "__all__"

    def create(self, validated_data):
        product_items = validated_data.pop('productItems', None)
        product_instance = product.objects.create(createtime=datetime.now, updatetime=datetime.now,belongs=self.context['request'].user, **validated_data)
        main_image_id_list = validated_data.pop('images', None)
        for id in main_image_id_list:
            product_image = productImage.objects.get(pk=id) # 查找前端已经上传的图片信息
            if product_image is not None:
                if product_image.productid is not None: # 确保是绑定新上传的图片，防止恶意更改
                    product_image.productid = product_instance
                    product_image.type = 0
                    product_image.save()
        for product_item_data in product_items:
            item_image_id_list = product_item_data.pop('images', None)
            product_item = productItem.objects.create(product=product_instance, **product_item_data)
            for id in item_image_id_list:
                product_item_image = productImage.objects.get(pk=id)
                if product_item_image is not None:
                    if product_image.productid is not None: # 确保是新上传的图片，防止恶意更改
                        product_item_image.productid = product_instance
                        product_item_image.product_item_id = product_item
                        product_item_image.type = 1
                        product_item_image.save()
        return product_instance

    def update(self, instance, validated_data):
        product_items = validated_data.pop('productItems', None)
        main_image_id_list = validated_data.pop('images', None)

        # 更新商品主属性相关信息
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.updatetime = datetime.now()
        instance.categoryid = validated_data.get('categoryid', instance.categoryid)
        instance.attributes = validated_data.get('attributes', instance.attributes)
        instance.brand = validated_data.get('brand', instance.brand)
        instance.yijiandaifa = validated_data.get('yijiandaifa', instance.yijiandaifa)
        instance.newup = validated_data.get('newup', instance.newup)
        instance.scene = validated_data.get('scene', instance.scene)

        # 首先剔除已经不存在的SKU
        id_list = list(filter(lambda item: item is not None, map(lambda item: item.get('id', None), product_items)))
        old_product_items = productItem.objects.filter(Q(product=instance))
        old_id_list = list(map(lambda item: item.id, old_product_items))
        removed_id_list = list(set(old_id_list) - set(id_list))
        productItem.objects.filter(id__in=removed_id_list).delete()

        # 开始遍历处理
        for item in product_items:
            item_id = item.get('id', None)
            if item_id is None:
                # 即为新增加的sku，添加新的sku
                productItem.objects.create(product=instance, **item)
            else:
                if item_id in removed_id_list:
                    # 如果该id为已删除id则跳过
                    pass
                else:
                    # 此处都为新增加的sku
                    product_item_instance = productItem.objects.get(pk=item_id)
                    product_item_instance.price = item.get('price', product_item_instance.price)
                    product_item_instance.attributes = item.get('attributes', product_item_instance.attributes)
                    product_item_instance.onshell = item.get('onshell', product_item_instance.onshell)
                    product_item_instance.favouredprice = item.get('favouredprice', product_item_instance.favouredprice)
                    product_item_instance.save()
        return instance

class tagsSerializer(ModelSerializer):
    class Meta:
        model=tags
        fields ="__all__"

