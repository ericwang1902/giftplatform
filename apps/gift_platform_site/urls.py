from django.urls import path
from apps.gift_platform_site.views import LoginView,RegView1,RegView2,uploadImg
from apps.gift_platform_site.views import index


app_name = 'gift_platform_site'

urlpatterns =  [
    path('sign/login', LoginView.as_view(), name="login"),
    path('sign/register1',RegView1.as_view(),name="reg1"),
    path('sign/register2',RegView2.as_view(),name="reg2"),
    path('sign/uploadimg',uploadImg.as_view(),name="uploadimg"),
    path('home', index)
]

