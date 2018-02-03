from django.urls import path

from .views import privateareaList,privateareaDetail
from .views import groupList,groupDetail
from .views import adminstratorList,adminstratorDetail
from .views import GiftDealersList,GiftDealerDetail
from .views import supplierList,supplierDetail

app_name = "users"

urlpatterns = [

    path('private-areas',privateareaList.as_view(),name= "privatelist"),
    path('private-areas/<int:pk>',privateareaDetail.as_view(),name="privatedetail"),

    path('groups',groupList.as_view(),name = "grouplist"),
    path('groups/<int:pk>',groupDetail.as_view(),name = "groupdetail"),

    path('adminstrators',adminstratorList.as_view(),name="adminstratorlist"),
    path('adminstrators/<int:pk>',adminstratorDetail.as_view(),name="adminstratordetail"),

    path('gift-dealers',GiftDealersList.as_view(),name='giftdealerslist'),
    path('gift-dealers/<int:pk>',GiftDealerDetail.as_view(),name='giftdealerdetail'),

    path('suppliers',supplierList.as_view(),name="suppliersList"),
    path('suppliers/<int:pk>',supplierDetail.as_view(),name='supplierDetail')

]