from users.models import privatearea
from  rest_framework.serializers import ModelSerializer
from  rest_framework import serializers


class privateareaSerialzer(ModelSerializer):
    class Meta:
        model = privatearea
        fields = '__all__'

