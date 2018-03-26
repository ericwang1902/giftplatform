from django.urls import path,include,re_path
from gift_platform_site.views import LoginView

app_name = 'gift_platform_site'

urlpatterns =  [
    path('sign/login', LoginView.as_view(), name="login")
]

