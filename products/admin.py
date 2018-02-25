from django.contrib import admin
from viplevels.models import  vipFunction
from .models import (category, product)

# Register your models here.
admin.site.register(vipFunction)

admin.site.register(category)
admin.site.register(product)
