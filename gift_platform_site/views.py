from django.shortcuts import render
from django.contrib.auth import authenticate,login
from django.views import View

class LoginView(View):
    def get(self, request):
        return render(request,"sign/login.html")

    def post(self, request):
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            # 如果用户不为空，则继续检查该账户类型，只能由商户登录进入
            if user.type is 'giftcompany':
                login(request, user)
            else:
                return render(request, 'sign/login.html', {
                    'error_message': "用户名或者密码错误"
                })
        else:
            # 用户名或者密码错误
            return render(request, 'sign/login.html', {
                'error_message': "用户名或者密码错误"
            })

