# _*_ coding:utf-8 _*_

__author__ = 'ericwang'
__date__ = '2018/1/22 8:31'

from .models import books
from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import Permission,Group,User

class bookSerilizer(ModelSerializer):
    class Meta:
        model= books
        fields = ('bookname')


class permissionSerializer(ModelSerializer):
    class Meta:
        model = Permission
        fields = ('name','content_type','codename')


class groupSerializer(ModelSerializer):
    class Meta:
        module= Group
        fields = ('name','permissions')

class userSerializer(ModelSerializer):
    class Meta:
        module = User
        fields = ('username','first_name','last_name','email','password',)