from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from ..models import Advertising


class AdvertisingSerializer(ModelSerializer):
    """
    广告的serializer
    """
    class Meta:
        model = Advertising
        fields= '__all__'

