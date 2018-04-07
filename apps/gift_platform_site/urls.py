from django.urls import path
from apps.gift_platform_site.views import LoginView,RegView1,RegView2,RegView3
from apps.gift_platform_site.views import IndexView
from apps.gift_platform_site.views import MyaccountView,ModifyPwdView,logoutView, brands_list, categories_list, category_product_list, root_category_product_list
from apps.gift_platform_site.views import msgCenterView

app_name = 'gift_platform_site'

urlpatterns =  [
    path('sign/login', LoginView.as_view(), name="login"),
    path('sign/logout',logoutView.as_view(),name="logoutv"),
    path('sign/register1',RegView1.as_view(),name="reg1"),
    path('sign/register2',RegView2.as_view(),name="reg2"),
    path('sign/reg3', RegView3.as_view(), name="reg3"),

    path('home/', IndexView.as_view(),name="home"),
    path('product/brands', brands_list),
    path('product/categories', categories_list),
    path('product/categories/<int:parent_category_id>/products', root_category_product_list, name="root_category_product_list"),
    path('product/categories/<int:parent_category_id>/<int:child_category_id>/products', category_product_list, name="category_product_list"),

    path('msgcenter/',msgCenterView.as_view(),name="msgcenter"),

    path('usercenter/myaccount',MyaccountView.as_view(),name='myaccount'),
    path('usercenter/mpwd',ModifyPwdView.as_view(),name="modifypwd"),

]

