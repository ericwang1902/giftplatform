# _*_ coding:utf-8 _*_

__author__ = 'ericwang'
__date__ = '2018/2/2 18:42'

from  rest_framework import generics,mixins
from .serializers import brandSerializer,categorySerializer,productSerializer,tagsSerializer
from products.models import brands,category,product,tags
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import filters
from django.db.models import Q

class brandsList(generics.GenericAPIView,mixins.ListModelMixin,mixins.CreateModelMixin):
    queryset = brands.objects.all()
    serializer_class = brandSerializer

    def get(self,request,*args,**kwargs):
        return self.list(request,*args,**kwargs)

    def post(self,request,*args,**kwargs):
        return self.create(request,*args,**kwargs)

class brandsDetail(generics.GenericAPIView,mixins.RetrieveModelMixin,mixins.UpdateModelMixin,mixins.DestroyModelMixin):
    queryset = brands.objects.all()
    serializer_class = brandSerializer

    def get(self,request,*args,**kwargs):
        print(args)
        return self.retrieve(request,*args,**kwargs)


    def put(self,request,*args,**kwargs):
        return self.update(request,*args,**kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class categoryList(generics.GenericAPIView,mixins.ListModelMixin,mixins.CreateModelMixin):
    queryset = category.objects.all()
    serializer_class = categorySerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class categoryDetail(generics.GenericAPIView,mixins.RetrieveModelMixin,mixins.UpdateModelMixin,mixins.DestroyModelMixin):
    queryset = category.objects.all()
    serializer_class = categorySerializer

    def get(self,request,*args,**kwargs):
        print(args)
        return self.retrieve(request,*args,**kwargs)


    def put(self,request,*args,**kwargs):
        return self.update(request,*args,**kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)



#需要修改~~~~~~~~~~~
class subcategoryList(generics.ListAPIView,generics.CreateAPIView):
    queryset = category.objects.all()
    serializer_class = categorySerializer

    def get_queryset(self):
        p=self.kwargs.get('parent', None)
        queryset = self.queryset.filter(parent=p)
        print(queryset)
        return queryset

    def perform_create(self, serializer):
        serializer.save(category=self.request.data)



class subcategoryDetail(generics.RetrieveAPIView,generics.UpdateAPIView,generics.DestroyAPIView):
    queryset = category.objects.all()
    serializer_class = categorySerializer

    def get_object(self):
        pk=self.kwargs.get('pk',None)
        parent = self.kwargs.get('parent',None)

        obj = get_object_or_404(self.queryset,parent=parent,id=pk)
        return obj

    def perform_update(self, serializer):
        instance = serializer.save()

    def perform_destroy(self, instance):
        pk = self.kwargs.get('pk', None)
        parent = self.kwargs.get('parent', None)
        category.objects.filter(id=pk,parent=parent).update(isdelete=0)

#供应商/产品接口,根据供应商id获取该供应商的产品列表
class supplierProdcutsList(generics.ListAPIView):
    queryset = product.objects.all()
    serializer_class = productSerializer

    def get_queryset(self):
        pk = self.kwargs.get('pk',None)
        queryset = self.queryset.filter(belongs=pk)
        return queryset

class supplierProductDetail(generics.RetrieveAPIView,generics.UpdateAPIView,generics.DestroyAPIView):
    queryset = product.objects.all()
    serializer_class = productSerializer

    def get_object(self):
        supplierid = self.kwargs.get('pk',None)
        productid = self.kwargs.get('productid',None)
        obj = get_object_or_404(self.queryset,belongs = supplierid,id = productid)
        return obj

    def perform_update(self, serializer):
        instance = serializer.save()

    def perform_destroy(self, instance):
        supplierid = self.kwargs.get('pk', None)
        productid = self.kwargs.get('productid', None)
        category.objects.filter(id=productid,belongs=supplierid).update(isdelete=0)

#tags
class tagsList(generics.GenericAPIView,mixins.ListModelMixin,mixins.CreateModelMixin):
    queryset = tags.objects.all()
    serializer_class = tagsSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('tagname',)

    def get_queryset(self):
        queryset = tags.objects.all()
        tagname = self.request.query_params.get('tagname', None)
        if tagname is not None:
            queryset = queryset.filter(Q(tagname=tagname))
        return queryset

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class tagsDetail(generics.GenericAPIView,mixins.RetrieveModelMixin,mixins.UpdateModelMixin,mixins.DestroyModelMixin):
    queryset = tags.objects.all()
    serializer_class = tagsSerializer

    def get(self,request,*args,**kwargs):
        print(args)
        return self.retrieve(request,*args,**kwargs)


    def put(self,request,*args,**kwargs):
        return self.update(request,*args,**kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)