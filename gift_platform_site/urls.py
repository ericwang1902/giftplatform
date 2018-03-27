from django.urls import path,include,re_path
from gift_platform_site.views import LoginView,RegView1


app_name = 'gift_platform_site'

urlpatterns =  [
    path('sign/login', LoginView.as_view(), name="login"),
    path('sign/register1',RegView1.as_view(),name="reg1")
]

