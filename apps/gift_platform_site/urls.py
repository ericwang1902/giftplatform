from django.urls import path
from apps.gift_platform_site.views import LoginView,RegView1,RegView2,RegView3
from apps.gift_platform_site.views import IndexView, new_private_supplier
from apps.gift_platform_site.views import MyaccountView,ModifyPwdView,logoutView, brands_list, categories_list, category_product_list, root_category_product_list, search_products
from apps.gift_platform_site.views import search_supplier, CartView, product_details

from apps.gift_platform_site.views import msgCenterView,sysinfoView,findpwdView,protocolView,delete_from_cart,export_ppt,brands_product_list,one_send_product_list, PrivateSupplier
from  apps.gift_platform_site.views import msgdetailView, edit_private_supplier,sysinfodetailView
from django.views.generic.base import RedirectView

app_name = 'gift_platform_site'

urlpatterns =  [
    path('', RedirectView.as_view(url='/home/', permanent=False), name="index"),
    path('accounts/login/',LoginView.as_view()),
    path('sign/login', LoginView.as_view(), name="login"),
    path('sign/logout',logoutView.as_view(),name="logoutv"),
    path('sign/register1',RegView1.as_view(),name="reg1"),
    path('sign/register2',RegView2.as_view(),name="reg2"),
    path('sign/reg3', RegView3.as_view(), name="reg3"),
    path('sign/findpwd',findpwdView.as_view(),name="findpwd"),

    path('home/', IndexView.as_view(),name="home"),
    path('cart/', CartView.as_view(), name="cart"),
    path('cart/<int:product_id>', delete_from_cart, name="cart_delete"),
    path('cart/export', export_ppt, name="export_ppt"),
    path('product/brands', brands_list),
    path('product/brands/<int:brand_id>', brands_product_list, name="brand_product_list"),
    path('product/categories', categories_list),
    path('product/categories/<int:parent_category_id>/products', root_category_product_list, name="root_category_product_list"),
    path('product/categories/<int:parent_category_id>/<int:child_category_id>/products', category_product_list, name="category_product_list"),
    path('product/search', search_products, name="search_products"),
    path('product/onesend', one_send_product_list, name="one_send_products"),
    path('product/<int:product_id>', product_details, name="product_details"),
    path('supplier/search', search_supplier, name="search_supplier"),

    path('msgcenter/',msgCenterView.as_view(),name="msgcenter"),
    path('msgdetail/',msgdetailView.as_view(),name='msgdetail'),

    path('usercenter/myaccount',MyaccountView.as_view(),name='myaccount'),
    path('usercenter/mpwd',ModifyPwdView.as_view(),name="modifypwd"),
    path('usercenter/sysinfo',sysinfoView.as_view(),name='sysinfo'),
    path('usercenter/sysinfodetail',sysinfodetailView.as_view(),name="sysinfodetail"),


    path('usercenter/privatearea/suppliers',PrivateSupplier.as_view(),name='private_suppliers'),
    path('usercenter/privatearea/suppliers/new',new_private_supplier,name='new_private_suppliers'),
    path('usercenter/privatearea/suppliers/<int:supplier_id>/edit',edit_private_supplier,name='edit_private_suppliers'),

    path('protocol/',protocolView.as_view(),name='protocol')


]

