from django.contrib import admin
from apps.viplevels.models import  vipFunction
from .models import (category, product, tags, brands)

# Register your models here.
admin.site.register(vipFunction)

admin.site.register(category)
admin.site.register(product)
admin.site.register(tags)
admin.site.register(brands)
