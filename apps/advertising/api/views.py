from rest_framework import mixins,generics
from ..models import Advertising
from ..api.serializers import AdvertisingSerializer


class AdvertisingList(generics.ListCreateAPIView):
    """
    广告列表和创建
    """
    queryset = Advertising.objects.all()
    serializer_class = AdvertisingSerializer


class AdvertisingDetails(generics.RetrieveUpdateAPIView):
    """
    广告列表的修改和详情
    """
    serializer_class = AdvertisingSerializer
