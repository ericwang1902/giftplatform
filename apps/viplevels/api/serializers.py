# _*_ coding:utf-8 _*_

__author__ = 'ericwang'
__date__ = '2018/2/12 8:41'

from apps.viplevels.models import (vipLevel, vipFunction)
from rest_framework.serializers import ModelSerializer

class viplevelsSerializer(ModelSerializer):
    class Meta:
        model = vipLevel
        fields = "__all__"

class VipFunctionsSerializer(ModelSerializer):
    class Meta:
        model = vipFunction
        fields = ("id", "functionname")