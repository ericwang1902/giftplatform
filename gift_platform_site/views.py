from django.shortcuts import render
from django.contrib.auth import authenticate,login
from django.views import View
from django.contrib.auth.backends import ModelBackend
from users.models import UserProfile
from django.db.models import Q

#支持手机号或者用户名登陆
class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            print(username)
            print(password)
            user = UserProfile.objects.get(Q(username=username)|Q(mobile=username))
            print( user.check_password(password))
            if user.check_password(password):
                return user
        except  Exception as e:
            return None


class LoginView(View):
    def get(self, request):
        return render(request,"sign/login.html")

    def post(self, request):
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            # 如果用户不为空，则继续检查该账户类型，只能由商户登录进入
            if user.type is 'giftcompany':
                login(request, user)
                print("登陆成功")
            else:
                return render(request, 'sign/login.html', {
                    'error_message': "用户名或者密码错误"
                })
        else:
            # 用户名或者密码错误
            return render(request, 'sign/login.html', {
                'error_message': "用户名或者密码错误"
            })

class RegView1(View):
    def get(self,request):
        return render(request,"sign/register1.html")

    def post(self,request):
        return render(request, "sign/register1.html")


class RegView2(View):
    def get(self,request):
        return render(request, "sign/register2.html")

