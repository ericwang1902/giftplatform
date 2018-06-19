from django.urls import path


from .views import privateareaList,privateareaDetail
from .views import groupList,groupDetail
from .views import adminstratorList,adminstratorDetail
from .views import GiftDealersList,GiftDealerDetail
from .views import supplierList,supplierDetail
from .views import permissionList
from .views import AuthInfoList
from .views import PermissionListOfMe
from .views import update_gift_dealer_vip_level
from .views import supplier_info
from .views import SiteMessageDetails,SiteMessageList, update_site_message_status
from .views import CustomJSONWebTokenAPIView
from .views import ServiceList
from .views import private_info, PrivateSupplierList

app_name = "users"

urlpatterns = [
    path('auth-info', AuthInfoList.as_view(),name="authInfoList"),

    path('site-messages', SiteMessageList.as_view(), name= "sitemessage_list"),
    path('site-messages/<int:pk>', SiteMessageDetails.as_view(), name="sitemessage_details"),
    path('site-messages/<int:message_id>/status', update_site_message_status, name="sitemessage_status"),

    path('private-areas',privateareaList.as_view(),name= "privatelist"),
    path('private-areas/<int:pk>',privateareaDetail.as_view(),name="privatedetail"),
    path('private-areas/<int:privatearea_id>/info',private_info, name="privatedetailInfo"),
    path('private-areas/<int:privatearea_id>/suppliers',PrivateSupplierList.as_view(), name="privatedetail_suppliers"),

    path('me/permissions', PermissionListOfMe.as_view(),name="permission_of_me"),

    path('permissionlist/',permissionList.as_view(),name="permissionlist"),

    path('groups',groupList.as_view(),name = "grouplist"),
    path('groups/<int:pk>',groupDetail.as_view(),name = "groupdetail"),

    path('adminstrators',adminstratorList.as_view(),name="adminstratorlist"),
    path('adminstrators/<int:pk>',adminstratorDetail.as_view(),name="adminstratordetail"),

    path('gift-dealers',GiftDealersList.as_view(),name='giftdealerslist'),
    path('gift-dealers/<int:pk>',GiftDealerDetail.as_view(),name='giftdealerdetail'),

    path('gift-dealers/<int:gift_company_id>/vip',update_gift_dealer_vip_level,name='giftdealervipupdate'),

    path('suppliers/me', supplier_info, name="mySupplierInfo"),
    path('suppliers',supplierList.as_view(),name="suppliersList"),
    path('suppliers/<int:pk>',supplierDetail.as_view(),name='supplierDetail'),

    path('service', ServiceList.as_view(), name="serviceList")

]