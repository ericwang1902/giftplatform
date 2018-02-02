from django.urls import path

from .views import privateareaList,privateareaDetail
from .views import groupList

app_name = "users"

urlpatterns = [

    path('private-areas',privateareaList.as_view(),name= "privatelist"),
    path('private-areas/<int:pk>',privateareaDetail.as_view(),name="privatedetail"),

    path('groups',groupList.as_view(),name = "grouplist"),
    path('groups/<int:pk>',groupList.as_view(),name = "groupdetail")
]