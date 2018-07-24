from rest_framework import mixins,generics
from apps.gift_platform_site.models import Invitation
from apps.invitation.api.serializers import InvitationSerializer
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from rest_framework import filters


class InvitationList(generics.ListAPIView,mixins.ListModelMixin):
    """
    邀请列表
    """
    queryset = Invitation.objects.all()
    serializer_class =  InvitationSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    pagination_class = PageNumberPagination
    pagination_class.page_size = 10

    def get(self,request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
