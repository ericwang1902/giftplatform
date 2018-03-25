from django.shortcuts import render
from django.contrib.auth import authenticate
from django.views import View

class LoginView(View):
    def get(self, request):
        return render(request,"sign/login.html")

    def post(self, request):
        pass

