# _*_ coding:utf-8 _*_

__author__ = 'ericwang'
__date__ = '2018/2/2 18:42'

from django.urls import path

from .views import brandsList,brandsDetail

from .views import categoryList,categoryDetail,subcategoryList,subcategoryDetail

from .views import supplierProdcutsList,subcategoryDetail

from  .views import tagsList,tagsDetail

from .views import ProductsList,ProductDetails,ProductImageUploaderView

app_name="products"

urlpatterns=[
    path('products/image', ProductImageUploaderView.as_view()),
    path('products/', ProductsList.as_view()),

    path('products/<int:id>', ProductDetails.as_view()),

    path('brands/',brandsList.as_view(),name="productslist"),
    path('brands/<int:pk>',brandsDetail.as_view(),name="productdetail"),

    path('categories',categoryList.as_view(),name="categorylist"),
    path('categories/<int:pk>',categoryDetail.as_view(),name="categorydetail"),

    path('categories/<int:parent>/categories',subcategoryList.as_view(),name="subcategorylist"),
    path('categories/<int:parent>/categories/<int:pk>', subcategoryDetail.as_view(), name="subcategorydetail"),

    path('suppliers/<int:pk>/goods',supplierProdcutsList.as_view(),name="supplisergoodslist"),
    path('suppliers/<int:pk>/goods/<int:productid>',subcategoryDetail.as_view(),name="supplisergoodsdetail"),

    path('tags',tagsList.as_view(),name="tagslist"),
    path('tags/<int:pk>',tagsDetail.as_view(),name="tagsdetail")


]