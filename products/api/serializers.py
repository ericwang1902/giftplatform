# _*_ coding:utf-8 _*_

__author__ = 'ericwang'
__date__ = '2018/2/2 18:41'

from products.models import brands,category,product,tags
from rest_framework.serializers import ModelSerializer

class brandSerializer(ModelSerializer):
    class Meta:
        model = brands
        fields = "__all__"

class categorySerializer(ModelSerializer):
    class Meta:
        model = category
        fields = "__all__"

class productSerializer(ModelSerializer):
    class Meta:
        model =product
        fields = "__all__"

class tagsSerializer(ModelSerializer):
    class Meta:
        model=tags
        fields ="__all__"

