# _*_ coding:utf-8 _*_

__author__ = 'ericwang'
__date__ = '2018/2/2 18:42'

from  rest_framework import generics,mixins
from .serializers import brandSerializer,categorySerializer,ProductSerializer,tagsSerializer,ProductImageUploaderSerializer
from apps.products.models import brands,category,product,tags,productImage,productItem
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import filters
from rest_framework import status
from django.db.models import Q
from rest_framework.parsers import MultiPartParser
from rest_framework.views import APIView
from giftplatform.settings import MEDIA_ROOT
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
import os, uuid

class ProductDescriptionMedia(APIView):

    def post(self, request, format=None):
        file = request.FILES["file"]
        dest_folder = os.path.join(MEDIA_ROOT, 'products/description/')
        if not os.path.exists(dest_folder):
            os.makedirs(dest_folder)
        filename = '{0}_{1}'.format(uuid.uuid4(), file.name)
        with open(os.path.join(dest_folder, filename), 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
        return Response({'success': True, 'msg': 'ok', 'file_path': ('http://' + request.get_host() + '/media/products/description/{0}'.format(filename))})


class brandsList(generics.GenericAPIView,mixins.ListModelMixin,mixins.CreateModelMixin):
    queryset = brands.objects.all().filter(isdelete=False)
    serializer_class = brandSerializer
    parser_classes = (MultiPartParser,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    pagination_class = PageNumberPagination
    pagination_class.page_size = 10

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
        kwargs['partial'] = True
        return self.update(request,*args,**kwargs)

    def perform_destroy(self, instance):
        pk = self.kwargs.get('pk', None)
        brands.objects.filter(id=pk).update(isdelete=True)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class UnlimitPagination(LimitOffsetPagination):
    default_limit =  100000


class AllCategoryList(generics.GenericAPIView, mixins.ListModelMixin):
    """
    返回所有的父分组
    """
    queryset = category.objects.all().filter(Q(isroot=True) & Q(isdelete=False))
    serializer_class = categorySerializer
    pagination_class = UnlimitPagination

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class AllSubCategoryList(generics.GenericAPIView, mixins.ListModelMixin):
    """
    返回所有的子分组列表
    """
    queryset = category.objects.all().filter(isdelete=False)
    serializer_class = categorySerializer
    pagination_class = UnlimitPagination

    def get_queryset(self):
        p=self.kwargs.get('parent', None)
        queryset = self.queryset.filter(parent=p)
        search_string = self.request.GET.get('search', None)
        if search_string is not None and search_string != '':
            queryset = queryset.filter(name=search_string)
        return queryset

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class categoryList(generics.GenericAPIView,mixins.ListModelMixin,mixins.CreateModelMixin):
    queryset = category.objects.all().filter(Q(isroot=True) & Q(isdelete=False))
    serializer_class = categorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    pagination_class = PageNumberPagination
    pagination_class.page_size = 10

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class categoryDetail(generics.GenericAPIView,mixins.RetrieveModelMixin,mixins.UpdateModelMixin,mixins.DestroyModelMixin):
    queryset = category.objects.all()
    serializer_class = categorySerializer

    def get(self,request,*args,**kwargs):
        return self.retrieve(request,*args,**kwargs)


    def put(self,request,*args,**kwargs):
        kwargs['partial'] = True
        return self.update(request,*args,**kwargs)

    def perform_destroy(self, instance):
        pk = self.kwargs.get('pk', None)
        category.objects.filter(id=pk).update(isdelete=True)
        category.objects.filter(parent_id=pk).update(isdelete=True)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)



class subcategoryList(generics.ListAPIView,generics.CreateAPIView):
    queryset = category.objects.all().filter(isdelete=False)
    serializer_class = categorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    pagination_class = PageNumberPagination
    pagination_class.page_size = 10


    def get_queryset(self):
        p=self.kwargs.get('parent', None)
        queryset = self.queryset.filter(parent=p)
        search_string = self.request.GET.get('search', None)
        if search_string is not None and search_string != '':
            queryset = queryset.filter(name=search_string)
        return queryset

    def perform_create(self, serializer):
        upper_id = self.kwargs.get('parent', None)
        if upper_id is not None:
            parent_category = category.objects.get(pk=upper_id)
        serializer.save(parent=parent_category)



class subcategoryDetail(generics.RetrieveAPIView,generics.UpdateAPIView,generics.DestroyAPIView):
    queryset = category.objects.all()
    serializer_class = categorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)

    def get_object(self):
        pk=self.kwargs.get('pk',None)
        parent = self.kwargs.get('parent',None)

        obj = get_object_or_404(self.queryset,parent=parent,id=pk)
        return obj

    def put(self,request,*args,**kwargs):
        kwargs['partial'] = True
        return self.update(request,*args,**kwargs)

    def perform_destroy(self, instance):
        pk = self.kwargs.get('pk', None)
        parent = self.kwargs.get('parent', None)
        category.objects.filter(id=pk,parent=parent).update(isdelete=True)

#商品创建统一接口
class ProductImageUploaderView(generics.CreateAPIView):
    serializer_class = ProductImageUploaderSerializer

class ProductsList(generics.ListCreateAPIView):
    queryset = product.objects.all().filter(isdelete=False)
    serializer_class = ProductSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    pagination_class = PageNumberPagination
    pagination_class.page_size = 10

    def perform_create(self, serializer):
        if self.request.user.inprivatearea:
            serializer.save(inprivatearea=True, privatearea=self.request.user.privatearea)
        else:
            serializer.save()

    def create(self, request, *args, **kwargs):
        data = dict.copy(request.data)
        images = data.pop("images", None)
        data["images"] = []
        for image_id in images:
            image = productImage.objects.get(pk=image_id)
            if image is not None:
                data["images"].append(image)
        for item in data["productItems"]:
            item_images = item.pop("images", None)
            item["images"] = []
            for image_id in item_images:
                image = productImage.objects.get(pk=image_id)
                if image is not None:
                    item["images"].append(image)
        brand_id = data.pop("brand", None)
        if brand_id is not None:
            data["brand"] = brands.objects.get(pk=brand_id)
        scenes_ids = data.pop("scenes", None)
        if scenes_ids is not None:
            data["scenes"] = list(map(lambda id:tags.objects.get(pk=id), scenes_ids))
        category_id = data.pop("category", None)
        if category_id is not None:
            data["category"] = category.objects.get(pk=category_id)
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def get_queryset(self):
        queryset = self.queryset.filter(belongs=self.request.user)
        return queryset

class ProductDetails(generics.RetrieveAPIView,generics.UpdateAPIView,generics.DestroyAPIView):
    queryset = product.objects.all()
    serializer_class = ProductSerializer

    def get_object(self):
        productid = self.kwargs.get('id',None)
        obj = get_object_or_404(self.queryset,belongs = self.request.user,id = productid)
        return obj

    def update(self, request, *args, **kwargs):
        data = dict.copy(request.data)
        images = data.pop("images", None)
        if images is not None:
            data["images"] = []
            for image_id in images:
                image = productImage.objects.get(pk=image_id)
                if image is not None:
                    data["images"].append(image)
        if "productItems" in data:
            for item in data["productItems"]:
                item_images = item.pop("images", None)
                item["images"] = []
                for image_id in item_images:
                    image = productImage.objects.get(pk=image_id)
                    if image is not None:
                        item["images"].append(image)

        brand_id = data.pop("brand", None)
        if brand_id is not None:
            data["brand"] = brands.objects.get(pk=brand_id)
        scenes_ids = data.pop("scenes", None)
        if scenes_ids is not None:
            data["scenes"] = list(map(lambda id:tags.objects.get(pk=id), scenes_ids))
        category_id = data.pop("category", None)
        if category_id is not None:
            data["category"] = category.objects.get(pk=category_id)

        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        if getattr(instance, '_prefetched_objects_cache', None):
        # If 'prefetch_related' has been applied to a queryset, we need to
        # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}
        return Response(serializer.data)

    def perform_destroy(self, instance):
        instance.isdelete = True
        productItem.objects.filter(product=instance).update(isdelete = True)
        instance.save()


#供应商/产品接口,根据供应商id获取该供应商的产品列表
class supplierProdcutsList(generics.ListAPIView):
    queryset = product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = PageNumberPagination
    pagination_class.page_size = 10

    def get_queryset(self):
        queryset = self.queryset.filter(belongs=self.request.user)
        return queryset

class supplierProductDetail(generics.RetrieveAPIView,generics.UpdateAPIView,generics.DestroyAPIView):
    queryset = product.objects.all()
    serializer_class = ProductSerializer

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
    pagination_class = PageNumberPagination
    pagination_class.page_size = 10

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