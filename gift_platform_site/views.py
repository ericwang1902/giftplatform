from django.shortcuts import render
from django.contrib.auth import authenticate,login
from django.views import View
from django.contrib.auth.backends import ModelBackend
from users.models import UserProfile
from django.db.models import Q
from django.contrib.auth.hashers import make_password
from . import forms

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
        usertype = request.GET.get("type")
        return render(request, "sign/register2.html",{"usertype":usertype})
    def post(self,request):
        regForm = forms.regForm(request.POST)
        if regForm.is_valid():
            username = request.POST.get('username')
            mobile  = request.POST.get('mobile')
            checkcode = request.POST.get('checkcode')
            email = request.POST.get('email')
            password = request.POST.get('pwd1')
            password2 = request.POST.get('pwd2')
            usertype = request.POST.get('usertype')
            if usertype != '1' and usertype != '2':
                print("用户类型错误！")

            #校验验证码逻辑
            if checkcode :
                #校验重复输入的密码逻辑
                if password == password2:
                    userInstance = UserProfile()
                    userInstance.username = username
                    userInstance.mobile = mobile
                    userInstance.email = email
                    userInstance.password =make_password(password)
                    if usertype == '1':
                        userInstance.type="supplier"
                    elif usertype =='2':
                        userInstance.type="giftcompany"
                    userInstance.save()
                    ###写跳转
                else:
                    print("两次输入的密码不相同")

            else:
                print("验证码错误，页面要显示出错误")
        else:
            print("表单有错误")

