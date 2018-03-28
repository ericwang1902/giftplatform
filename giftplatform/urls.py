"""giftplatform URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include,re_path
from apps.users.api.views import ObtainJSONWebToken
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    # token,post方法获取token
    path('api-token-auth/', ObtainJSONWebToken.as_view()),
    # rest framework 的viewset都会在这里进行认证
    re_path(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    path('admin/', admin.site.urls),

    path('api/', include('apps.permissionapi.urls')),

    path('api/', include('apps.users.api.urls')),

    path('api/', include('apps.products.api.urls')),

    path('api/', include('apps.viplevels.api.urls')),

    path('', include('apps.gift_platform_site.urls'))


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
