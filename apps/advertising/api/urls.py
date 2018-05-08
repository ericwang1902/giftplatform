from django.urls import path
from .views import AdvertisingList, AdvertisingDetails

app_name = "advertising"

urlpatterns = [
    path('advertising',AdvertisingList.as_view(),name='advertisinglist'),
    path('advertising/<int:pk>',AdvertisingDetails.as_view(),name='advertisingdetail'),
]
