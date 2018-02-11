from  rest_framework import generics,mixins

from .serializers import privateareaSerialzer,groupSerialzer,userprofileSerializer,permissionSerializer

from users.models import privatearea,UserProfile

from django.contrib.auth.models import Permission,Group

from django.db.models import Q

from rest_framework import filters
from rest_framework.pagination import PageNumberPagination


class privateareaList(generics.GenericAPIView,mixins.ListModelMixin,mixins.CreateModelMixin):
    queryset = privatearea.objects.all()
    serializer_class = privateareaSerialzer

    def get(self,request,*args,**kwargs):
        return self.list(request,*args,**kwargs)

    def post(self,request,*args,**kwargs):
        return self.create(request,*args,**kwargs)




class privateareaDetail(generics.GenericAPIView,mixins.RetrieveModelMixin,mixins.UpdateModelMixin,mixins.DestroyModelMixin):
    queryset = privatearea.objects.all()
    serializer_class = privateareaSerialzer

    def get(self,request,*args,**kwargs):
        print(args)
        print(kwargs)
        return self.retrieve(request,*args,**kwargs)


    def put(self,request,*args,**kwargs):
        return self.update(request,*args,**kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

class permissionList(generics.GenericAPIView,mixins.ListModelMixin):
    queryset = Permission.objects.all()
    serializer_class =permissionSerializer
    pagination_class = PageNumberPagination
    pagination_class.page_size = 1000

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class groupList(generics.GenericAPIView,mixins.ListModelMixin,mixins.CreateModelMixin):
    queryset = Group.objects.all()
    serializer_class = groupSerialzer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class groupDetail(generics.GenericAPIView,mixins.RetrieveModelMixin,mixins.UpdateModelMixin,mixins.DestroyModelMixin):
    queryset = Group.objects.all()
    serializer_class = groupSerialzer

    def get(self,request,*args,**kwargs):
        return self.retrieve(request,*args,**kwargs)


    def put(self,request,*args,**kwargs):
        return self.update(request,*args,**kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


#管理员用来查询系统管理员和客服人员的所有帐号信息
class adminstratorList(generics.ListAPIView,generics.CreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = userprofileSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username', 'mobile', 'email')

    def get_queryset(self):
        queryset = self.queryset.filter(Q(type='admin') |Q(type="service"))
        username = self.request.query_params.get('username', None)
        if username is not None:
            queryset = queryset.filter(Q(username=username))
        return queryset

    def perform_create(self, serializer):
        serializer.save(type='admin')


class adminstratorDetail(generics.GenericAPIView,mixins.RetrieveModelMixin,mixins.UpdateModelMixin,mixins.DestroyModelMixin):
    queryset = UserProfile.objects.all()
    serializer_class = userprofileSerializer

    def get(self,request,*args,**kwargs):
        return self.retrieve(request,*args,**kwargs)


    def put(self,request,*args,**kwargs):
        kwargs['partial'] = True
        return self.update(request,*args,**kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

#礼品公司
class GiftDealersList(generics.ListAPIView,generics.CreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = userprofileSerializer

    def get_queryset(self):
        queryset = self.queryset.filter(Q(type='giftcompany'))
        return queryset

    def perform_create(self, serializer):
        serializer.save(category=self.request.data)

class GiftDealerDetail(generics.GenericAPIView,mixins.RetrieveModelMixin,mixins.UpdateModelMixin,mixins.DestroyModelMixin):
    queryset = UserProfile.objects.all()
    serializer_class = userprofileSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

#供应商
class supplierList(generics.ListAPIView,generics.CreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = userprofileSerializer

    def get_queryset(self):
        queryset = self.queryset.filter(Q(type='supplier'))
        return queryset

    def perform_create(self, serializer):
        serializer.save(category=self.request.data)

class supplierDetail(generics.GenericAPIView,mixins.RetrieveModelMixin,mixins.UpdateModelMixin,mixins.DestroyModelMixin):
    queryset = UserProfile.objects.all()
    serializer_class = userprofileSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
