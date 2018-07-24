from rest_framework import serializers
from apps.gift_platform_site.models import Invitation


class InvitationSerializer(serializers.ModelSerializer):
    """
    邀请序列化类
    """
    class Meta:
        model = Invitation
        fields = ('id', 'company_name', 'name', 'job_position', 'tel', 'email', 'created_at')
