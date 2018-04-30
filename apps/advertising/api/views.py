from rest_framework import mixins,generics
from ..models import Advertising
from ..api.serializers import AdvertisingSerializer


class AdvertisingList(generics.ListCreateAPIView):
    """
    广告列表和创建
    """
    queryset = Advertising.objects.all()
    serializer_class = AdvertisingSerializer

    def perform_create(self, serializer):
        serializer.save(publisher=self.request.user)


class AdvertisingDetails(generics.RetrieveUpdateDestroyAPIView):
    """
    广告列表的修改和详情
    """
    serializer_class = AdvertisingSerializer

    def perform_destroy(self, instance):
        instance.is_deleted = True # 软删除
        instance.save()

    def put(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request,*args,**kwargs)
