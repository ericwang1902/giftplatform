# _*_ coding:utf-8 _*_

__author__ = 'ericwang'
__date__ = '2018/1/22 8:31'

from .models import books
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from django.contrib.auth.models import Permission,Group
from users.models import UserProfile


class bookSerilizer(ModelSerializer):
    class Meta:
        model= books
        #fields = ('bookname')
        fields = '__all__'



class permissionSerializer(ModelSerializer):
    class Meta:
        model = Permission
        fields = ('name','content_type','codename')
        depth = 3



class groupSerializer(ModelSerializer):
    permissions =serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    class Meta:
        model= Group
        fields = ('name','permissions')

class userSerializer(ModelSerializer):
    #groups = serializers.PrimaryKeyRelatedField(many=True,read_only=True)
    #groups = groupSerializer(source='group_set',many=True)
    class Meta:
        model = UserProfile
        fields = ('username','first_name','last_name','email','password','groups')
        depth =2

