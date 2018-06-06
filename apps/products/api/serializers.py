# _*_ coding:utf-8 _*_

__author__ = 'ericwang'
__date__ = '2018/2/2 18:41'

from apps.products.models import brands,category,product,tags,productItem,productImage
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from datetime import datetime
from django.db.models import Q


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
    images = ProductImageUploaderSerializer(many=True, read_only=True)

    class Meta:
        model = productItem
        fields = "__all__"

class tagsSerializer(ModelSerializer):
    class Meta:
        model=tags
        fields ="__all__"


class ProductSerializer(ModelSerializer):
    productItems = ProductItemSerializer(many=True)
    brand = brandSerializer(read_only=True)
    scenes = tagsSerializer(many=True, read_only=True)
    category = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()

    def get_images(self, obj):
        request = self.context.get('request')
        images = obj.images.filter(type=0)
        serializer = ProductImageUploaderSerializer(instance=images, many=True)
        data = serializer.data
        for item in data:
            item['productimage'] = request.build_absolute_uri(item['productimage'])
        return data;

    def get_category(self, obj):
        """
        因为只有两层所以此处暂定为两层结构
        返回分组数组，数组结构为[parent, child]
        :param obj:
        :return:
        """
        if obj.categoryid is not None:
            return [{ "id": obj.categoryid.parent.id, "name" : obj.categoryid.parent.name}, {"id": obj.categoryid.id, "name": obj.categoryid.name}]

    def run_validation(self, data):
        return data

    class Meta:
        model = product
        fields = "__all__"

    def create(self, validated_data):
        product_items = validated_data.pop('productItems', None)
        main_images = validated_data.pop('images', None)
        scenes = validated_data.pop('scenes', None)
        category = validated_data.pop('category', None)
        product_instance = product.objects.create(createtime=datetime.now, updatetime=datetime.now,belongs=self.context['request'].user, **validated_data)
        if category is not None:
            product_instance.categoryid = category
            product_instance.save()
        if scenes is not None:
            for scene in scenes:
                product_instance.scenes.add(scene)
            product_instance.save()
        for product_image in main_images:
            if product_image.productid is None: # 确保是绑定新上传的图片，防止恶意更改
                product_image = productImage.objects.get(pk=product_image.id)
                product_image.productid = product_instance
                product_image.type = 0
                product_image.save()
        for product_item_data in product_items:
            item_images = product_item_data.pop('images', None)
            product_item = productItem.objects.create(product=product_instance, **product_item_data)
            for product_item_image in item_images:
                if product_item_image.productid is None: # 确保是新上传的图片，防止恶意更改
                    product_item_image.productid = product_instance
                    product_item_image.product_item_id = product_item
                    product_item_image.type = 1
                    product_item_image.save()
        return product_instance

    def update(self, instance, validated_data):
        """
        更新过程逻辑：
        1. 更新产品主信息内容
        2. 更新主图信息
        3. 更新sku信息时，优先拉出原有的skuid列表,然后检查是否有sku已被删除，如果有sku已被删除则优先批量删除sku，随后将没有id的传入值做新增处理，最后更新已有的sku信息
        """
        product_items = validated_data.pop('productItems', None)
        main_images = validated_data.pop('images', None)
        scenes = validated_data.pop('scenes', None)
        category = validated_data.pop('category', None)

        # 更新场景标签
        if scenes is not None:
            instance.scenes.clear()
            for scene in scenes:
                instance.scenes.add(scene)
            instance.save()
        # 分组更新
        if category is not None:
            instance.categoryid = category
            instance.save()

        # 更新商品主属性相关信息
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.updatetime = datetime.now()
        instance.categoryid = validated_data.get('category', instance.categoryid)
        instance.attributes = validated_data.get('attributes', instance.attributes)
        instance.brand = validated_data.get('brand', instance.brand)
        instance.yijiandaifa = validated_data.get('yijiandaifa', instance.yijiandaifa)
        instance.newup = validated_data.get('newup', instance.newup)
        instance.simple_description = validated_data.get('simple_description', instance.simple_description)
        instance.model = validated_data.get('model', instance.model)

        # 开始删除所有已经不使用的product image
        old_product_main_image_items = productImage.objects.filter(Q(productid=instance, product_item_id=None))
        old_product_image_ids = list(map(lambda item: item.id, old_product_main_image_items))
        product_main_image_ids = list(map(lambda item: item.id, main_images))
        product_main_image_removed_id_list = list(set(old_product_image_ids) - set(product_main_image_ids))
        for main_image in productImage.objects.filter(id__in=product_main_image_removed_id_list):
            main_image.productid = None
            main_image.product_item_id = None
            main_image.save()

        # 更新商品主图
        for product_image in main_images:
            product_image = productImage.objects.get(pk=product_image.id)
            product_image.productid = instance
            product_image.product_item_id = None
            product_image.type = 0
            product_image.save()

        # 首先剔除已经不存在的SKU
        id_list = list(filter(lambda item: item is not None, map(lambda item: item.get('id', None), product_items)))
        old_product_items = productItem.objects.filter(Q(product=instance))
        old_id_list = list(map(lambda item: item.id, old_product_items))
        removed_id_list = list(set(old_id_list) - set(id_list))
        productItem.objects.filter(id__in=removed_id_list).delete()


        # 开始遍历处理
        for item in product_items:
            item_id = item.get('id', None)
            item_images = item.pop('images', None)
            if item_id is None: # id 为空，即为新增
                # 即为新增加的sku，添加新的sku
                product_item = productItem.objects.create(product=instance, **item)
                for product_item_image in item_images:
                    if product_item_image.productid is None: # 确保是新上传的图片，防止恶意更改
                        product_item_image.productid = instance
                        product_item_image.product_item_id = product_item
                        product_item_image.type = 1
                        product_item_image.save()
            else:
                if item_id in removed_id_list:
                    # 如果该id为已删除id则跳过
                    pass
                else:
                    # 此处都为更新过的
                    product_item_instance = productItem.objects.get(pk=item_id)
                    product_item_instance.price = item.get('price', product_item_instance.price)
                    product_item_instance.attributes = item.get('attributes', product_item_instance.attributes)
                    product_item_instance.onshell = item.get('onshell', product_item_instance.onshell)
                    product_item_instance.favouredprice = item.get('favouredprice', product_item_instance.favouredprice)
                    product_item_instance.stock = item.get('stock', product_item_instance.stock)

                    # 开始处理已经不使用的sku图
                    old_product_item_image_items = productImage.objects.filter(Q(productid=instance, product_item_id=product_item_instance))
                    old_product_item_image_ids = list(map(lambda item: item.id, old_product_item_image_items))
                    product_item_image_ids = list(map(lambda item: item.id, item_images))
                    product_item_image_removed_id_list = list(set(old_product_item_image_ids) - set(product_item_image_ids))
                    for item_image in productImage.objects.filter(id__in=product_item_image_removed_id_list):
                        item_image.productid = None
                        item_image.product_item_id = None
                        item_image.save()

                    # 更新新的sku图
                    for product_item_image in item_images:
                        product_item_image.productid = instance
                        product_item_image.product_item_id = product_item_instance
                        product_item_image.type = 1
                        product_item_image.save()
                    product_item_instance.save()
        instance.save()
        return instance

