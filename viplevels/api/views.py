# _*_ coding:utf-8 _*_

__author__ = 'ericwang'
__date__ = '2018/2/12 8:42'

from viplevels.api.serializers import viplevelsSerializer
from rest_framework import generics,mixins
from viplevels.models import vipLevel
from rest_framework import filters
from django.db.models import Q

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

    def post(self,request,*args,**kwargs):
        return self.create(request,*args,**kwargs)

class viplevelDetail(generics.GenericAPIView,mixins.RetrieveModelMixin,mixins.DestroyModelMixin,mixins.UpdateModelMixin):
    queryset = vipLevel.objects.all()
    serializer_class = viplevelsSerializer

    def get(self,request,*args,**kwargs):
        return self.retrieve(request,*args,**kwargs)

    def put(self,request,*args,**kwargs):
        return self.update(request,*args,**kwargs)

    def delete(self,request,*args,**kwargs):
        return self.destroy(request,*args,**kwargs)

