from django.urls import path
from apps.gift_platform_site.views import LoginView,RegView1,RegView2,RegView3
from apps.gift_platform_site.views import indexView
from apps.gift_platform_site.views import MyaccountView,ModifyPwdView


app_name = 'gift_platform_site'

urlpatterns =  [
    path('sign/login', LoginView.as_view(), name="login"),
    path('sign/register1',RegView1.as_view(),name="reg1"),
    path('sign/register2',RegView2.as_view(),name="reg2"),
    path('sign/reg3', RegView3.as_view(), name="reg3"),

    path('home/', indexView.as_view(),name="home"),

    path('usercenter/myaccount',MyaccountView.as_view(),name='myaccount'),
    path('usercenter/mpwd',ModifyPwdView.as_view(),name="modifypwd")
]

