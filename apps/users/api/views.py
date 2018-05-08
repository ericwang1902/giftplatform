from rest_framework import generics, mixins

from .serializers import privateareaSerialzer, groupSerialzer, userprofileSerializer, permissionSerializer, AuthInfoSerializer, SupplierSerializer, SiteMessageSerializer

from apps.users.models import privatearea, UserProfile, userAuthinfo, vipLevelChangeHistory, siteMessge
from apps.viplevels.models import vipLevel

from django.contrib.auth.models import Permission, Group

from django.db.models import Q

from rest_framework import filters
from rest_framework.pagination import PageNumberPagination
from django.db import transaction
from rest_framework.exceptions import PermissionDenied
from rest_framework_jwt.views import JSONWebTokenAPIView
from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.serializers import JSONWebTokenSerializer
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
from rest_framework.decorators import  api_view
from rest_framework.exceptions import NotFound, APIException
from dateutil import parser

jwt_response_payload_handler = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER


class CustomJSONWebTokenAPIView(JSONWebTokenAPIView):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            user = serializer.object.get('user') or request.user

            # 如果该用户为供应商，并且该供应商在私有域中，如果该私有域停用则禁止登录
            if user.inprivatearea == True and user.type == 'supplier':
                if user.privatearea.status == 1:
                    return Response({ 'message': 'forbiden login' }, status = status.HTTP_403_FORBIDDEN)

            token = serializer.object.get('token')
            response_data = jwt_response_payload_handler(token, user, request)
            response = Response(response_data)
            user.last_login = datetime.now()
            user.save()
            if api_settings.JWT_AUTH_COOKIE:
                expiration = (datetime.utcnow() +
                              api_settings.JWT_EXPIRATION_DELTA)
                response.set_cookie(api_settings.JWT_AUTH_COOKIE,
                                    token,
                                    expires=expiration,
                                    httponly=True)
            return response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ObtainJSONWebToken(CustomJSONWebTokenAPIView):
    """
    API View that receives a POST with a user's username and password.
    Returns a JSON Web Token that can be used for authenticated requests.
    """
    serializer_class = JSONWebTokenSerializer


class privateareaList(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin):
    queryset = privatearea.objects.all()
    serializer_class = privateareaSerialzer

    def get(self, request, *args, **kwargs):
        if request.user.has_perm('users.list_privatearea'):
            return self.list(request, *args, **kwargs)
        else:
            raise PermissionDenied()

    def perform_create(self, serializer):
        with transaction.atomic():
            giftdealer_id = self.request.data.pop('userId', None)
            privatearea_instance = serializer.save()
            giftdealer = UserProfile.objects.get(pk=giftdealer_id)
            giftdealer.inprivatearea = True
            giftdealer.privatearea = privatearea_instance
            giftdealer.save()

    def post(self, request, *args, **kwargs):
        if request.user.has_perm('users.add_privatearea'):
            return self.create(request, *args, **kwargs)
        else:
            raise PermissionDenied()


class privateareaDetail(generics.GenericAPIView, mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
                        mixins.DestroyModelMixin):
    queryset = privatearea.objects.all()
    serializer_class = privateareaSerialzer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        if request.user.has_perm('users.add_privatearea'):
            kwargs['partial'] = True
            return self.update(request, *args, **kwargs)
        else:
            raise PermissionDenied()

    def delete(self, request, *args, **kwargs):
        if request.user.has_perm('users.delete_privatearea'):
            return self.destroy(request, *args, **kwargs)
        else:
            raise PermissionDenied()

class PermissionListOfMe(generics.GenericAPIView, mixins.ListModelMixin):
    queryset = Permission.objects.all()
    serializer_class = permissionSerializer
    pagination_class = None

    def get_queryset(self):
        username = self.request.user.username
        user = UserProfile.objects.get(username=username)
        if user is not None:
            if user.is_superuser:
                return Permission.objects.all()
            group = user.groups.all().first()
            return group.permissions
        else:
            return None

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class permissionList(generics.GenericAPIView, mixins.ListModelMixin):
    queryset = Permission.objects.all()
    serializer_class = permissionSerializer
    pagination_class = PageNumberPagination
    pagination_class.page_size = 1000

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class groupList(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin):
    queryset = Group.objects.all()
    serializer_class = groupSerialzer

    def get(self, request, *args, **kwargs):
        if request.user.has_perm('auth.list_group'):
            return self.list(request, *args, **kwargs)
        else:
            raise PermissionDenied()

    def post(self, request, *args, **kwargs):
        if request.user.has_perm('auth.add_group'):
            return self.create(request, *args, **kwargs)
        else:
            raise PermissionDenied()


class groupDetail(generics.GenericAPIView, mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin):
    queryset = Group.objects.all()
    serializer_class = groupSerialzer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        if request.user.has_perm('auth.change_group'):
            return self.update(request, *args, **kwargs)
        else:
            raise PermissionDenied()

    def delete(self, request, *args, **kwargs):
        if request.user.has_perm('auth.delete_group'):
            return self.destroy(request, *args, **kwargs)
        else:
            raise PermissionDenied()


# 管理员用来查询系统管理员和客服人员的所有帐号信息
class adminstratorList(generics.ListAPIView, generics.CreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = userprofileSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username', 'mobile', 'email')

    def get(self, request, *args, **kwargs):
        if request.user.has_perm('users.list_userprofile'):
            return self.list(request, *args, **kwargs)
        else:
            raise PermissionDenied()

    def get_queryset(self):
        queryset = self.queryset.filter(Q(type='admin') | Q(type="service"))
        username = self.request.query_params.get('username', None)
        if username is not None:
            queryset = queryset.filter(Q(username=username))
        return queryset

    def post(self, request, *args, **kwargs):
        if request.user.has_perm('users.add_userprofile'):
            return self.create(request,*args,**kwargs)
        else:
            raise PermissionDenied()

    def perform_create(self, serializer):
        serializer.save(type='admin')


class adminstratorDetail(generics.GenericAPIView, mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
                         mixins.DestroyModelMixin):
    queryset = UserProfile.objects.all()
    serializer_class = userprofileSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        if request.user.has_perm('users.change_userprofile'):
            kwargs['partial'] = True
            return self.update(request, *args, **kwargs)
        else:
            raise PermissionDenied()

    def delete(self, request, *args, **kwargs):
        if request.user.has_perm('users.delete_userprofile'):
            return self.destroy(request, *args, **kwargs)
        else:
            raise PermissionDenied()


# 礼品公司
class GiftDealersList(generics.ListAPIView, generics.CreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = userprofileSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username', 'mobile', 'email')

    def get(self, request, *args, **kwargs):
        if request.user.has_perm('users.list_giftdealer'):
            return self.list(request, *args, **kwargs)
        else:
            raise PermissionDenied()

    def get_queryset(self):
        queryset = self.queryset.filter(Q(type='giftcompany'))
        username = self.request.query_params.get('username', None)
        inprivatearea = self.request.query_params.get('inprivatearea', None)
        is_auth = self.request.query_params.get('is_auth', None)
        if is_auth is not None:
            if is_auth.lower() == 'true':
                queryset = queryset.filter(Q(authStatus=True))
            else:
                queryset = queryset.filter(Q(authStatus=False))
        if username is not None:
            queryset = queryset.filter(Q(username=username))
        if inprivatearea is not None:
            if inprivatearea.lower() == 'true':
                queryset = queryset.filter(Q(inprivatearea=True))
            else:
                queryset = queryset.filter(Q(inprivatearea=False))
        return queryset

    def post(self, request, *args, **kwargs):
        if request.user.has_perm('users.add_giftdealer'):
            return self.create(request, *args, **kwargs)
        else:
            raise PermissionDenied()

    def perform_create(self, serializer):
        servicestaff_id = self.request.data.pop('servicestaff', None)
        viplevel_id = self.request.data.pop('viplevel', None)
        if not viplevel_id:
            viplevel_id = None
        if not servicestaff_id:
            servicestaff_id = None
        servicestaff = None
        viplevel = None
        if servicestaff_id is not None:
            servicestaff = UserProfile.objects.get(id=servicestaff_id)
        if viplevel_id is not None:
            viplevel = vipLevel.objects.get(id=viplevel_id)
        serializer.save(type='giftcompany', servicestaff=servicestaff, viplevel=viplevel)


class GiftDealerDetail(generics.GenericAPIView, mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
                       mixins.DestroyModelMixin):
    queryset = UserProfile.objects.all()
    serializer_class = userprofileSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def perform_update(self, serializer):
        servicestaff_id = self.request.data.pop('servicestaff', None)
        viplevel_id = self.request.data.pop('viplevel', None)
        if not viplevel_id:
            viplevel_id = None
        if not servicestaff_id:
            servicestaff_id = None
        servicestaff = None
        viplevel = None
        if servicestaff_id is not None:
            servicestaff = UserProfile.objects.get(id=servicestaff_id)
        if viplevel_id is not None:
            viplevel = vipLevel.objects.get(id=viplevel_id)
        serializer.save(servicestaff=servicestaff, viplevel=viplevel)

    def put(self, request, *args, **kwargs):
        if request.user.has_perm('users.change_giftdealer'):
            kwargs['partial'] = True
            return self.update(request, *args, **kwargs)
        else:
            raise PermissionDenied()

    def delete(self, request, *args, **kwargs):
        if request.user.has_perm('users.delete_giftdealer'):
            return self.destroy(request, *args, **kwargs)
        else:
            raise PermissionDenied()


# 供应商
class supplierList(generics.ListAPIView, generics.CreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = SupplierSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username', 'mobile', 'email')

    def get(self, request, *args, **kwargs):
        if request.user.has_perm('users.list_supplier'):
            return self.list(request, *args, **kwargs)
        else:
            raise PermissionDenied()

    def perform_create(self, serializer):
        servicestaff_id = self.request.data.pop('servicestaff', None)
        if not servicestaff_id:
            servicestaff_id = None
        servicestaff = None
        if servicestaff_id is not None:
            servicestaff = UserProfile.objects.get(id=servicestaff_id)
        serializer.save(type='supplier', servicestaff=servicestaff)

    def post(self, request, *args, **kwargs):
        if request.user.has_perm('users.add_supplier'):
            return self.create(request, *args, **kwargs)
        else:
            raise PermissionDenied()

    def get_queryset(self):
        queryset = self.queryset.filter(Q(type='supplier'))
        is_auth = self.request.query_params.get('is_auth', None)
        if is_auth is not None:
            if is_auth.lower() == 'true':
                queryset = queryset.filter(Q(authStatus=True))
            else:
                queryset = queryset.filter(Q(authStatus=False))
        return queryset

class supplierDetail(generics.GenericAPIView, mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin):
    queryset = UserProfile.objects.all()
    serializer_class = SupplierSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def perform_update(self, serializer):
        servicestaff_id = self.request.data.pop('servicestaff', None)
        if not servicestaff_id:
            servicestaff_id = None
        servicestaff = None
        if servicestaff_id is not None:
            servicestaff = UserProfile.objects.get(id=servicestaff_id)
        serializer.save(servicestaff=servicestaff)


    def put(self, request, *args, **kwargs):
        if request.user.has_perm('users.change_supplier'):
            kwargs['partial'] = True
            return self.update(request, *args, **kwargs)
        else:
            raise PermissionDenied()

    def delete(self, request, *args, **kwargs):
        if request.user.has_perm('users.delete_supplier'):
            return self.destroy(request, *args, **kwargs)
        else:
            raise PermissionDenied()


class SiteMessageList(generics.ListCreateAPIView):
    """
    站内公告的相关功能
    """
    queryset = siteMessge.objects.filter(isdelete = False)
    serializer_class = SiteMessageSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if request.user.is_staff == False: # 如果不是管理员则只能看到自己的公告列表
            queryset = queryset.filter(fromuser = request.user)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(fromuser = self.request.user)


class SiteMessageDetails(generics.RetrieveUpdateDestroyAPIView):
    """
    站内公告详情的相关功能
    """
    queryset = siteMessge.objects.filter(isdelete = False)
    serializer_class = SiteMessageSerializer

    def perform_destroy(self, instance):
        if not self.request.user.is_staff: # 非管理员删除则需要判断是否该消息属于操作者
            if instance.fromuser.id != self.request.user.id:
                raise PermissionDenied()
            else:
                instance.isdelete = True
                instance.save()


class AuthInfoList(generics.ListAPIView):
    queryset = userAuthinfo.objects.all()
    serializer_class = AuthInfoSerializer

    def get(self, request, *args, **kwargs):
        if request.user.has_perm('users.auth_supplier') or request.user.has_perm('users.auth_giftdealer'):
            return self.list(request, *args, **kwargs)
        else:
            raise PermissionDenied()

    def get_queryset(self):
        userid = self.request.query_params.get("userid", None)
        if userid is not None:
            queryset = self.queryset.filter(Q(userid=userid))
        return queryset

@api_view(['GET','PUT'])
def update_gift_dealer_vip_level(request, gift_company_id):
    """
    更新礼品上的充值会员信息
    :param request:
    :param gift_company_id:
    :return:
    """
    user = UserProfile.objects.get(pk=gift_company_id)
    if user is None:
        raise NotFound(detail="gift company not found", code=404)

    if user.type != "giftcompany":
        raise NotFound(detail="gift company not found", code=404)

    if request.method == 'PUT':
        vip_instance = vipLevel.objects.get(pk=request.data.get('viplevel', None))
        if vip_instance is not None:
            vip_record = vipLevelChangeHistory()
            vip_record.userid = user
            vip_record.orignallevel = user.viplevel
            vip_record.destlevel = vip_instance
            vip_record.start_time = parser.parse(request.data.get('start_time', None))
            vip_record.end_time = parser.parse(request.data.get('end_time', None))
            vip_record.save()
            user.viplevel = vip_instance
            user.save()
            return Response(userprofileSerializer(user).data, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "viplevel not existed"}, status=status.HTTP_400_BAD_REQUEST)

    latest_vip_change = vipLevelChangeHistory.objects.filter(userid=user).order_by('-id').first()
    return Response({
        "userId": user.id,
        "viplevel": latest_vip_change.destlevel.id,
        "startTime": latest_vip_change.start_time,
        "endTime": latest_vip_change.end_time
    })
