from django.urls import path,include,re_path
from gift_platform_site.views import LoginView

urlpatterns = [
    path('sign/login', LoginView.as_view())
]

