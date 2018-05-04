from rest_framework import mixins,generics, filters
from ..models import Advertising
from ..api.serializers import AdvertisingSerializer


class AdvertisingList(generics.ListCreateAPIView):
    """
    广告列表和创建
    """
    queryset = Advertising.objects.filter(is_deleted=False).all()
    serializer_class = AdvertisingSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('title',)

    def perform_create(self, serializer):
        position = self.request.POST.get('position')
        existed_advertising = Advertising.objects.filter(position=position).first()

        if existed_advertising is not None:
            existed_advertising.status = 1
            existed_advertising.save()
        serializer.save(publisher=self.request.user)


class AdvertisingDetails(generics.RetrieveUpdateDestroyAPIView):
    """
    广告列表的修改和详情
    """
    serializer_class = AdvertisingSerializer
    queryset = Advertising.objects.filter(is_deleted=False).all()

    def perform_destroy(self, instance):
        instance.is_deleted = True # 软删除
        instance.save()

    def put(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request,*args,**kwargs)
