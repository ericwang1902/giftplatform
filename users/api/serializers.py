from users.models import privatearea,UserProfile
from  rest_framework.serializers import ModelSerializer
from  rest_framework import serializers
from  django.contrib.auth.models import Permission,Group


class privateareaSerialzer(ModelSerializer):
    class Meta:
        model = privatearea
        fields = '__all__'

class groupSerialzer(ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'

class userprofileSerializer(ModelSerializer):
    class Meta:
        model = UserProfile
        fields='__all__'