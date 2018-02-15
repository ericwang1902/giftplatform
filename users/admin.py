from django.contrib import admin
from django.contrib.auth.models import Permission
from users.models import UserProfile, userAuthinfo


# Register your models here.
admin.site.register(Permission)
admin.site.register(UserProfile)
admin.site.register(userAuthinfo)
