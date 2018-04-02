from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login
from django.views import View
from django.contrib.auth.backends import ModelBackend
from apps.users.models import UserProfile
from apps.products.models import product,brands,category
from django.db.models import Q
from django.contrib.auth.hashers import make_password
from . import forms
from apps.users.models import userAuthinfo
from django.shortcuts import redirect
from django.contrib.auth import logout

class IndexView(View):
    def get(self,request):
        products = product.objects.filter(status=0)[0:16]
        return render(request, "home/index.html", { "products": products })

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
                #return redirect('/home')
                return redirect('/usercenter/myaccount')
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

            usertype='0'
            if request.POST.get('usertype'):
                request.session["usertype"] = request.POST.get('usertype')
                usertype = request.session["usertype"]
            else:
                usertype=request.session["usertype"]
            if usertype != '1' and usertype != '2':
                print("用户类型错误！")
                return redirect('/sign/register1')

            #增加判断用户名、手机号是否重复的逻辑
            #如果有该用户
            usernamecount=  UserProfile.objects.filter(username=username).count()
            if usernamecount>0:
                return render(request, 'sign/register2.html', {"wronginfousername": "已存在该用户名，请更换", "formsets": request.POST})
            mobilecount = UserProfile.objects.filter(mobile=mobile).count()
            if mobilecount>0:
                return render(request, 'sign/register2.html',
                          {"wronginfomobile": "已存在该手机号，请更换", "formsets": request.POST})

            #如果没有该用户
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

                    userins = UserProfile()
                    userins.username = username
                    userins.mobile =mobile
                    userins.email = email
                    userins.password = make_password(pwd1)
                    if usertype == '1':
                        request.session["usertype"] = "supplier"
                        userins.type = "supplier"

                    elif usertype =='2':
                        request.session["usertype"] = "giftcompany"
                        userins.type = "giftcompany"

                    userins.save()

                    return redirect('/sign/reg3')

                else:
                    return render(request, 'sign/register2.html',
                                  {"wronginfo": "两次输入的密码不相同", "formsets": request.POST})  #
            else:
                return render(request, 'sign/register2.html',
                              {"wronginfo2": "验证码错误", "formsets": request.POST})


        else:
            return  render(request, 'sign/register2.html', {"regForm":regForm, "formsets":request.POST})#form验证信息回显

class RegView3(View):
    def get(self,request):
        print(request.session["username"])
        return render(request,'sign/reg3.html')
    def post(self,request):

        username1 = request.session['username']
        usernow = UserProfile.objects.get(username=username1)
        # 接受图片上传逻辑
        reg2tpform = forms.reg2tpForm(request.POST,request.FILES)
        print(reg2tpform.is_valid())
        #判断是新上传，还是要替换原来老的上传的营业执照
        if reg2tpform.is_valid():
            try:#查询是否有记录，如果有就更新照片
                ui=userAuthinfo.objects.get(userid=usernow)
                yyzz = request.FILES.get('yyzz')
                ui.img = yyzz
                ui.save()
                return render(request, 'sign/reg3.html',
                              {"yyzz": ui.img.url,
                               "img1": yyzz
                               })
            except :#如果没有记录，就上传照片
                    userauthinfoInstance = userAuthinfo()
                    yyzz = request.FILES.get('yyzz')
                    userauthinfoInstance.img = yyzz
                    userauthinfoInstance.userid=usernow
                    userauthinfoInstance.save()

                    print('ss')
                    return render(request, 'sign/reg3.html',
                                  {"yyzz": userauthinfoInstance.img.url,
                                   "img1":yyzz
                                   })
        else:
            return render(request, 'sign/reg3.html', {"reg3Form": reg2tpform})  # form验证信息回显





class MyaccountView(View):
    def get(self,request):
        #获取当前登录的用户信息
        gender=True
        try:
            currentUser = request.user
            if currentUser.is_authenticated:
                if currentUser.gender:
                    gender=1
                else:
                    gender =0
                return render(request, 'usercenter/myaccount.html',{'currentuser':currentUser,'gender':gender})
            else:
                return redirect('/sign/login')
        except:
            return render(request, 'sign/login.html')


    def post(self,request):
        username = request.POST.get('username')
        gender = request.POST.get('gender')
        email = request.POST.get('email')

        userinfo =UserProfile.objects.get(username=request.user.username)
        userinfo.username = username
        if gender == '1':
            userinfo.gender = True
        else:
            userinfo.gender=False

        userinfo.email = email
        userinfo.save()

        return redirect('/usercenter/myaccount')


class ModifyPwdView(View):
    def get(self,request):
        gender = True
        try:
            currentUser = request.user
            if currentUser.is_authenticated:
                return render(request, 'usercenter/modifypassword.html')
            else:
                return redirect('/sign/login')
        except:
            return redirect('/sign/login')

    def post(self,request):
        mdform = forms.modifypwdform(request.POST)
        if mdform.is_valid():
            pwd = request.POST.get('pwd')
            newpwd1 = request.POST.get('newpwd1')
            newpwd2 = request.POST.get('newpwd2')

            user = authenticate(username=request.user.username, password=pwd)
            if user is not None:
                if newpwd1==newpwd2:
                    user.password = newpwd1
                    user.save()
                    logout(request)
                    #要一个render
                    return redirect('/sign/login')
                else:
                    errormessge1 = "两次输入的密码不一致"
                    return render(request,
                                  'usercenter/modifypassword.html',
                                  {'errormesg1': errormessge1})
            else:
                # 原密码错误
                errormessge = "密码错误"
                return render(request,
                              'usercenter/modifypassword.html',
                              {'errormesg': errormessge})
        else:
            return render(request,
                          'usercenter/modifypassword.html',
                          {'mdform': mdform})


class logoutView(View):
    def post(self,request):
        v = request.POST.get('logoutin')
        logout(request)
        return redirect('/sign/login')


def brands_list(request):
    """
    展示所有的品牌信息
    :param request:
    :return:
    """
    brands_list = brands.objects.all()
    return render(request, 'products/brands_list.html', { 'brands_list': brands_list })

def categories_list(request):
    """
    展示所有的分组信息
    :param request:
    :return:
    """
    categories_list = category.objects.filter(isroot = True) # 查找所有的根级分组
    return render(request, 'products/categories_list.html', { 'categories_list': categories_list  })