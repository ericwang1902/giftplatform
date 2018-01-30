from django.shortcuts import render

# Create your views here.

from rest_framework import generics,mixins
from .models import books

from .serializers import bookSerilizer,\
    permissionSerializer,\
    groupSerializer,userSerializer
from django.contrib.auth.models import Permission,Group
from users.models import UserProfile

class booklist(generics.GenericAPIView,
               mixins.ListModelMixin,
               mixins.CreateModelMixin):
    queryset = books.objects.all()
    serializer_class = bookSerilizer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self,request,*args,**kwargs):
        return self.create(request,*args,**kwargs)



class permissionList(generics.GenericAPIView,mixins.ListModelMixin):
    queryset = Permission.objects.all()
    serializer_class =permissionSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class groupList(generics.GenericAPIView,mixins.ListModelMixin):
    queryset = Group.objects.all()
    serializer_class = groupSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

class userList(generics.GenericAPIView,mixins.ListModelMixin):
    queryset = UserProfile.objects.all()
    serializer_class = userSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)