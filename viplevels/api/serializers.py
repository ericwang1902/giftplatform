# _*_ coding:utf-8 _*_

__author__ = 'ericwang'
__date__ = '2018/2/12 8:41'

from viplevels.models import vipLevel
from rest_framework.serializers import ModelSerializer

class viplevelsSerializer(ModelSerializer):
    class Meta:
        model = vipLevel
        fields = "__all__"
