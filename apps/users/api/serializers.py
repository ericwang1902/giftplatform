from apps.users.models import privatearea,UserProfile,userAuthinfo,supplier, siteMessge
from apps.products.models import product
from  rest_framework.serializers import ModelSerializer
from rest_framework import  serializers
from  django.contrib.auth.models import Permission,Group
from apps.viplevels.api.serializers import viplevelsSerializer
from django.db.models.fields import related_descriptors
from django.db.models import Q

class permissionSerializer(ModelSerializer):
    class Meta:
        model = Permission
        fields = "__all__"

class AuthInfoSerializer(ModelSerializer):
    class Meta:
        model = userAuthinfo
        fields = "__all__"

class privateareaSerialzer(ModelSerializer):
    supplier_count = serializers.SerializerMethodField('get_private_supplier_count')
    product_count = serializers.SerializerMethodField('get_private_product_count')

    def get_private_supplier_count(self, privatearea):
        supplier_count = supplier.objects.filter(userid__privatearea_id = privatearea.id).count()
        return supplier_count

    def get_private_product_count(self, privatearea):
        product_count = product.objects.filter(Q(privatearea_id = privatearea.id) & Q(isdelete=False)).count()
        return product_count

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

class SupplierShopInfoSerializer(ModelSerializer):
    class Meta:
        model = supplier
        fields = '__all__'

class SupplierSerializer(ModelSerializer):

    supplier = SupplierShopInfoSerializer(many=False)

    class Meta:
        model = UserProfile
        fields= '__all__'

    def create(self, validated_data):
        shop_info = validated_data.pop('supplier')
        user = super(SupplierSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        supplier.objects.create(userid=user, **shop_info)
        return user

    def update(self, instance, validated_data):
        shop_info = validated_data.pop('supplier', None)

        if shop_info is not None:
            try:
                instance.supplier.suppliername = shop_info.get('suppliername', None)
                instance.supplier.qq = shop_info.get('qq', None)
                instance.supplier.tel = shop_info.get('tel', None)
                instance.supplier.email = shop_info.get('email', None)
                instance.supplier.save()
            except supplier.DoesNotExist:
                instance.supplier = supplier.objects.create(userid=instance, **shop_info)

        user = super(SupplierSerializer, self).update(instance, validated_data)
        new_password = validated_data.get('password', None)
        if new_password is not None:
            user.set_password(new_password)
            user.save()
        return user

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

class SiteMessageSerializer(ModelSerializer):
    class Meta:
        model = siteMessge
        fields = ('id', 'title', 'content', 'publishdate', 'updatetime', 'status')



