# _*_ coding:utf-8 _*_

__author__ = 'ericwang'
__date__ = '2018/2/12 8:42'

from apps.viplevels.api.serializers import (viplevelsSerializer, VipFunctionsSerializer)
from rest_framework import generics,mixins
from apps.viplevels.models import (vipLevel, vipFunction, levelToFunction)
from rest_framework import filters
from django.db.models import Q
from django.db import transaction

class viplevelList(generics.GenericAPIView,mixins.ListModelMixin,mixins.CreateModelMixin):
    queryset = vipLevel.objects.all()
    serializer_class = viplevelsSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('vipname',)

    def get_queryset(self):
        queryset = vipLevel.objects.all()
        vipname = self.request.query_params.get('vipname', None)
        if vipname is not None:
            queryset = queryset.filter(Q(vipname=vipname))
        return queryset

    def get(self,request,*args,**kwargs):
        return self.list(request,*args,**kwargs)

    def perform_create(self, serializer):
        with transaction.atomic():
            vipfunction_id_array = self.request.data.pop('vipFunctions', None)
            vipfunctions = None
            if vipfunction_id_array is not None:
                vipfunctions = vipFunction.objects.filter(id__in=vipfunction_id_array)
            viplevel = serializer.save()
            if vipfunctions is not None:
                for vipfunction in vipfunctions:
                    level_through_function = levelToFunction.objects.create(viplevelid=viplevel, vipfunctionid=vipfunction)
                    level_through_function.save()

    def post(self,request,*args,**kwargs):
        return self.create(request,*args,**kwargs)

class viplevelDetail(generics.GenericAPIView,mixins.RetrieveModelMixin,mixins.DestroyModelMixin,mixins.UpdateModelMixin):
    queryset = vipLevel.objects.all()
    serializer_class = viplevelsSerializer

    def get(self,request,*args,**kwargs):
        return self.retrieve(request,*args,**kwargs)

    def perform_update(self, serializer):
        with transaction.atomic():
            vipfunction_id_array = self.request.data.pop('vipFunctions', None)
            vipfunctions = None
            if vipfunction_id_array is not None:
                vipfunctions = vipFunction.objects.filter(id__in=vipfunction_id_array)
            viplevel = serializer.save()
            levelToFunction.objects.filter(viplevelid=viplevel.id).delete()
            if vipfunctions is not None:
                for vipfunction in vipfunctions:
                    level_through_function = levelToFunction.objects.create(viplevelid=viplevel, vipfunctionid=vipfunction)
                    level_through_function.save()

    def put(self,request,*args,**kwargs):
        return self.update(request,*args,**kwargs)

    def delete(self,request,*args,**kwargs):
        return self.destroy(request,*args,**kwargs)

class VipFunctionsList(generics.GenericAPIView,mixins.ListModelMixin):
    queryset = vipFunction.objects.all()
    serializer_class = VipFunctionsSerializer

    def get(self,request,*args,**kwargs):
        return self.list(request,*args,**kwargs)
