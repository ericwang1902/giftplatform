from .views import InvitationList
from django.urls import path

app_name = "invitation"

urlpatterns=[
    path('invitations/', InvitationList.as_view())
]