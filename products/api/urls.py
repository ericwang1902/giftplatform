# _*_ coding:utf-8 _*_

__author__ = 'ericwang'
__date__ = '2018/2/2 18:42'

from django.urls import path

from .views import brandsList,brandsDetail

from .views import categoryList,categoryDetail,subcategoryList

app_name="products"

urlpatterns=[
    path('brands',brandsList.as_view(),name="productslist"),
    path('brands/<int:pk>',brandsDetail.as_view(),name="productdetail"),

    path('categories',categoryList.as_view(),name="categorylist"),
    path('categories/<int:pk>',categoryDetail.as_view(),name="categorydetail"),
    path('categories/<int:pk>/categories',subcategoryList.as_view(),name="subcategorylist")
]