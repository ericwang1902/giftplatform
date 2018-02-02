# _*_ coding:utf-8 _*_

__author__ = 'ericwang'
__date__ = '2018/2/2 18:42'

from  rest_framework import generics,mixins
from .serializers import brandSerializer,categorySerializer
from products.models import brands,category

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
class subcategoryList(generics.GenericAPIView,mixins.ListModelMixin,mixins.CreateModelMixin):
    queryset = category.objects.all()
    serializer_class = categorySerializer
    #lookup_fields = ['pk',]

    def get(self,request,*args,**kwargs):
        return self.list(request, *args, **kwargs)
