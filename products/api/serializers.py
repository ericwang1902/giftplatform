# _*_ coding:utf-8 _*_

__author__ = 'ericwang'
__date__ = '2018/2/2 18:41'

from products.models import brands,category
from rest_framework.serializers import ModelSerializer

class brandSerializer(ModelSerializer):
    class Meta:
        model = brands
        fields = "__all__"

class categorySerializer(ModelSerializer):
    class Meta:
        model = category
        fields = "__all__"

