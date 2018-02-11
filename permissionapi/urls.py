# _*_ coding:utf-8 _*_

__author__ = 'ericwang'
__date__ = '2018/1/22 8:32'

from django.urls import path,include,re_path
from .views import booklist,permissionList,groupList,userList

app_name="permissionapi"
urlpatterns = [
    # token
    path('booklist/',booklist.as_view(),name="booklist"),
   # path('permissionlist/',permissionList.as_view(),name="permissionlist"),
    path('grouplist/',groupList.as_view(),name="grouplist"),
    path('userlist/',userList.as_view(),name="userlist")

]