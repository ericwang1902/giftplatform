from django.urls import path
from apps.gift_platform_site.views import LoginView,RegView1,RegView2,RegView3
from apps.gift_platform_site.views import IndexView
from apps.gift_platform_site.views import MyaccountView,ModifyPwdView,logoutView, brands_list, categories_list, category_product_list, root_category_product_list, search_products
from apps.gift_platform_site.views import search_supplier

from apps.gift_platform_site.views import msgCenterView,sysinfoView,findpwdView,protocolView

app_name = 'gift_platform_site'

urlpatterns =  [
    path('accounts/login/',LoginView.as_view()),
    path('sign/login', LoginView.as_view(), name="login"),
    path('sign/logout',logoutView.as_view(),name="logoutv"),
    path('sign/register1',RegView1.as_view(),name="reg1"),
    path('sign/register2',RegView2.as_view(),name="reg2"),
    path('sign/reg3', RegView3.as_view(), name="reg3"),
    path('sign/findpwd',findpwdView.as_view(),name="findpwd"),

    path('home/', IndexView.as_view(),name="home"),
    path('product/brands', brands_list),
    path('product/categories', categories_list),
    path('product/categories/<int:parent_category_id>/products', root_category_product_list, name="root_category_product_list"),
    path('product/categories/<int:parent_category_id>/<int:child_category_id>/products', category_product_list, name="category_product_list"),
    path('product/search', search_products, name="search_products"),
    path('supplier/search', search_supplier, name="search_supplier"),

    path('msgcenter/',msgCenterView.as_view(),name="msgcenter"),

    path('usercenter/myaccount',MyaccountView.as_view(),name='myaccount'),
    path('usercenter/mpwd',ModifyPwdView.as_view(),name="modifypwd"),
    path('usercenter/sysinfo',sysinfoView.as_view(),name='sysinfo'),

    path('protocol/',protocolView.as_view(),name='protocol')

]

