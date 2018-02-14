from django.contrib import admin
from viplevels.models import  vipFunction
from .models import category

# Register your models here.
admin.site.register(vipFunction)

admin.site.register(category)
