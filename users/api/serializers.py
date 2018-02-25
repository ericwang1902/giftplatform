from users.models import privatearea,UserProfile,userAuthinfo
from  rest_framework.serializers import ModelSerializer
from  rest_framework import serializers
from  django.contrib.auth.models import Permission,Group
from viplevels.api.serializers import viplevelsSerializer

class permissionSerializer(ModelSerializer):
    class Meta:
        model = Permission
        fields = "__all__"

class AuthInfoSerializer(ModelSerializer):
    class Meta:
        model = userAuthinfo
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
    privatearea = privateareaSerialzer(read_only=True)
    class Meta:
        model = UserProfile
        fields='__all__'
    def create(self, validated_data):
        user = super(userprofileSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user
    def update(self, instance, validated_data):
        user = super(userprofileSerializer, self).update(instance, validated_data)
        new_password = validated_data.get('password', None)
        if new_password is not None:
            user.set_password(new_password)
            user.save()
        return user



