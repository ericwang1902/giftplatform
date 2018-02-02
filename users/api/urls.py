from django.urls import path

from .views import privateareaList,privateareaDetail

app_name = "users"

urlpatterns = [

    path('private-areas',privateareaList.as_view(),name= "privatelist")
]