from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login
from django.views import View
from django.contrib.auth.backends import ModelBackend
from apps.users.models import UserProfile
from django.db.models import Q
from django.contrib.auth.hashers import make_password
from . import forms
from apps.users.models import userAuthinfo

def index(request):
    """
    首页内容
    :param request:
    :return:
    """
    return render(request, "home/index.html")

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
        return render(request, "sign/login.html")

    def post(self, request):
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        print(user)
        if user is not None:
            # 如果用户不为空，则继续检查该账户类型，只能由商户登录进入
            print(user.type)
            if user.type == 'giftcompany':
                login(request, user)
                print("登陆成功")
                return redirect('')
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
        return render(request, "sign/register1.html")

    def post(self,request):
        return render(request, "sign/register1.html")

#传到session中
class RegView2(View):
    def get(self,request):
        usertype = request.GET.get("type")
        return render(request, "sign/register2.html", {"usertype":usertype})
    def post(self,request):
        regForm = forms.regForm(request.POST)
        if regForm.is_valid():
            username = request.POST.get('username')
            mobile  = request.POST.get('mobile')
            checkcode = request.POST.get('checkcode')
            email = request.POST.get('email')
            pwd1 = request.POST.get('pwd1')
            pwd2 = request.POST.get('pwd2')
            usertype = request.POST.get('usertype')
            if usertype != '1' and usertype != '2':
                print("用户类型错误！")

            #校验验证码逻辑
            if checkcode :
                #校验重复输入的密码逻辑
                if pwd1 == pwd2:
                    request.session["username"]= username
                    request.session["mobile"] = mobile
                    request.session["email"] = email
                    request.session["pwd1"] = pwd1
                    request.session["pwd2"] = pwd2
                    request.session["usertype"] = usertype
                    request.session['checkcode']=checkcode

                    if usertype == '1':
                        request.session["usertype"] = "supplier"
                    elif usertype =='2':
                        request.session["usertype"] = "giftcompany"

                    return render(request, 'sign/register2.html',
                                  {"formsets": request.session})

                else:
                    return render(request, 'sign/register2.html',
                                  {"wronginfo": "两次输入的密码不相同", "formsets": request.POST})  #


            else:
                print("验证码错误，页面要显示出错误")
        else:
            return  render(request, 'sign/register2.html', {"regForm":regForm, "formsets":request.POST})#form验证信息回显

class uploadImg(View):
    def post(self,request):
        # 接受图片上传逻辑
        print('test')
        reg2tpForm = forms.reg2tpForm(request.FILES)

        yyzz = request.FILES.get('yyzz')
        request.session["yyzz"]=yyzz


        # userauthinfoInstance = userAuthinfo()
        # if reg2tpForm.is_valid():
        #     # 存照片
        #     yyzz = request.FILES.get('yyzz')
        #     userauthinfoInstance.img = yyzz

#最终点击注册提交，讲session中暂存的数据进行提交
class RegFinal(View):
    def post(self,request):
        # userInstance = UserProfile()
        # userInstance.username = username
        # userInstance.mobile = mobile
        # userInstance.email = email
        # userInstance.password = make_password(pwd1)

        return 111
