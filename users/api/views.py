from rest_framework import generics, mixins

from .serializers import privateareaSerialzer, groupSerialzer, userprofileSerializer, permissionSerializer, AuthInfoSerializer
from viplevels.api.serializers import viplevelsSerializer
from rest_framework import serializers

from users.models import privatearea, UserProfile, userAuthinfo
from viplevels.models import vipLevel

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

jwt_response_payload_handler = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER


class CustomJSONWebTokenAPIView(JSONWebTokenAPIView):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            user = serializer.object.get('user') or request.user
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
            self.create(self,request,*args,**kwargs)
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
            return self.list(self, request, *args, **kwargs)
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
            return self.create(self, request, *args, **kwargs)
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
    serializer_class = userprofileSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username', 'mobile', 'email')

    def get(self, request, *args, **kwargs):
        if request.user.has_perm('users.list_supplier'):
            return self.list(self, request, *args, **kwargs)
        else:
            raise PermissionDenied()

    def post(self, request, *args, **kwargs):
        if request.user.has_perm('users.add_supplier'):
            return self.create(self, request, *args, **kwargs)
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

    def perform_create(self, serializer):
        serializer.save(type='supplier')


class supplierDetail(generics.GenericAPIView, mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin):
    queryset = UserProfile.objects.all()
    serializer_class = userprofileSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

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

class AuthInfoList(generics.ListAPIView):
    queryset = userAuthinfo.objects.all()
    serializer_class = AuthInfoSerializer

    def get(self, request, *args, **kwargs):
        if request.user.has_perm('users.auth_supplier') or request.user.has_perm('users.auth_giftdealer'):
            return self.list(self, request, *args, **kwargs)
        else:
            raise PermissionDenied()

    def get_queryset(self):
        userid = self.request.query_params.get("userid", None)
        if userid is not None:
            queryset = self.queryset.filter(Q(userid=userid))
        return queryset

