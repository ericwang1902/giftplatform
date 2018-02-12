# _*_ coding:utf-8 _*_

__author__ = 'ericwang'
__date__ = '2018/2/12 8:42'

from  django.urls import path

from .views import viplevelList,viplevelDetail

app_name = "viplevel"

urlpatterns=[
    path('viplevels',viplevelList.as_view(),name="viplevellist"),
    path('viplevels/<int:pk>',viplevelDetail.as_view(),name="vipleveldetail")
]