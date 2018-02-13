from users.models import privatearea,UserProfile
from  rest_framework.serializers import ModelSerializer
from  rest_framework import serializers
from  django.contrib.auth.models import Permission,Group
from viplevels.api.serializers import viplevelsSerializer

class permissionSerializer(ModelSerializer):
    class Meta:
        model = Permission
        fields = "__all__"

class privateareaSerialzer(ModelSerializer):
    class Meta:
        model = privatearea
        fields = '__all__'

class groupSerialzer(ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'

class ServiceStaffSerializer(ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'

class userprofileSerializer(ModelSerializer):
    viplevel = viplevelsSerializer(read_only=True)
    servicestaff = ServiceStaffSerializer(read_only=True)
    class Meta:
        model = UserProfile
        fields='__all__'



