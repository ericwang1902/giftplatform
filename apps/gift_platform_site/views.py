from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.views import View
from django.contrib.auth.backends import ModelBackend
from apps.users.models import UserProfile, supplier, siteMessge
from apps.products.models import product, brands, category, productItem
from django.db.models import Q
from django.contrib.auth.hashers import make_password
from . import forms
from apps.users.models import userAuthinfo
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.core.paginator import Paginator
from django.http import HttpResponseBadRequest, HttpResponseNotFound, HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
import json
from decimal import Decimal
from apps.gift_platform_site.libs.ppt_utils import generate_ppt
from django.conf import settings
import os
import datetime
from django.contrib import messages
import random,time
from publicModules.demo_sms_send import send_sms
import uuid


def home(request):
    """
    home界面，无任何模板，只是用来判断是否已经登录，如果登录则跳转至home/index，否则则跳转至登录界面
    :param request:
    :return:
    """
    pass


class IndexView(LoginRequiredMixin, View):
    def get(self, request):
        queryset = product.objects.filter(Q(status=0) & Q(isdelete=False))
        t = request.GET.get('t', '0')
        print(t)
        if t == '1':
            queryset = queryset.filter(productItems__onshell=True).distinct()
        queryset = queryset.order_by('-createtime')

        products = queryset[0:16]
        currentuser = request.user

        return render(request, "home/index.html", {"products": products, "currentuser": currentuser, "t": t})


# 支持手机号或者用户名登陆
class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            print(username)
            print(password)
            user = UserProfile.objects.get(Q(username=username) | Q(mobile=username))
            print(user.check_password(password))
            if user.check_password(password):
                return user
        except  Exception as e:
            return None


class LoginView(View):
    def get(self, request):
        next = request.GET.get('next')
        print(next)
        return render(request, "sign/login.html", {'next': next})

    def post(self, request):
        loginForm = forms.loginform(request.POST)
        if loginForm.is_valid():
            user = authenticate(username=request.POST['username'], password=request.POST['password'])
            print(user)
            if user is not None:  # 用户名和密码正确，且已经经过管理员审核操作,通过或者退回
                if user.currentpoint == 'bc':  # 管理员已经操作
                    if user.authStatus == True:  # 通过审核
                        if user.type == 'giftcompany':
                            login(request, user)
                            if request.POST.get('next') != 'None':
                                return redirect(request.POST.get('next'))
                            else:
                                return redirect('/home')
                        elif user.type == 'supplier':
                            return render(request, 'sign/login.html', {
                                'error_message': "供应商请从供应商入口登录"
                            })

                    else:  # 未通过审核
                        request.session['info'] = "未通过认证，请重新上传"
                        return redirect('/sign/login')
                else:  # user.currentpoint=='ck':#管理员尚未操作
                    return render(request, 'sign/login.html', {
                        'sh_message': "请等待审核通过后再进行登录"
                    })
            else:  # 用户名和密码错误
                return render(request, 'sign/login.html', {
                    'error_message': "用户名或者密码错误"
                })
        else:
            return render(request, 'sign/login.html', {
                'loginform': loginForm
            })


class RegView1(View):
    def get(self, request):
        return render(request, "sign/register1.html")

    def post(self, request):
        return render(request, "sign/register1.html")


# 传到session中
class RegView2(View):
    def get(self, request):
        usertype = request.GET.get("type")
        return render(request, "sign/register2.html", {"usertype": usertype})

    def post(self, request):
        regForm = forms.regForm(request.POST)
        if regForm.is_valid():
            username = request.POST.get('username')
            mobile = request.POST.get('mobile')
            checkcode = request.POST.get('checkcode')
            email = request.POST.get('email')
            pwd1 = request.POST.get('pwd1')
            pwd2 = request.POST.get('pwd2')

            usertype = request.GET.get("type")
            if usertype != '1' and usertype != '2':
                print("用户类型错误！")
                return redirect('/sign/register1')

            # 增加判断用户名、手机号是否重复的逻辑
            # 如果有该用户
            usernamecount = UserProfile.objects.filter(username=username).count()
            if usernamecount > 0:
                return render(request, 'sign/register2.html',
                              {"wronginfousername": "已存在该用户名，请更换", "formsets": request.POST})
            mobilecount = UserProfile.objects.filter(mobile=mobile).count()
            if mobilecount > 0:
                return render(request, 'sign/register2.html',
                              {"wronginfomobile": "已存在该手机号，请更换", "formsets": request.POST})

            # 如果没有该用户
            # 校验验证码逻辑
            if checkcode:
                # 校验重复输入的密码逻辑
                if pwd1 == pwd2:
                    request.session["username"] = username
                    request.session["mobile"] = mobile
                    request.session["email"] = email
                    request.session["pwd1"] = pwd1
                    request.session["pwd2"] = pwd2
                    request.session["usertype"] = usertype
                    request.session['checkcode'] = checkcode

                    userins = UserProfile()
                    userins.username = username
                    userins.mobile = mobile
                    userins.email = email
                    userins.password = make_password(pwd1)
                    if usertype == '1':
                        request.session["usertype"] = "supplier"
                        userins.type = "supplier"

                    elif usertype == '2':
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
            return render(request, 'sign/register2.html', {"regForm": regForm, "formsets": request.POST})  # form验证信息回显


def createPhoneCode(request):
        chars = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        x = random.choice(chars), random.choice(chars), random.choice(chars), random.choice(chars)
        verifyCode = "".join(x)
        request.session["phoneVerifyCode"] = {"time": int(time.time()), "code": verifyCode}
        print(verifyCode)
        return verifyCode

class verifyCodeView(View):
    def get(self,request):
        #生成验证码
        createPhoneCode(request)
        #发送验证码
        code = request.session["phoneVerifyCode"]
        print(code)
        __business_id = uuid.uuid1()
        # print(__business_id)
        params = "{\"code\":\"12345\"}"
        send_sms(__business_id, "17798885277", "一点科技", "SMS_134190252", params)


class RegView3(View):
    def get(self, request):
        print(request.session["username"])
        try:
            info = request.session['info']
            return render(request, 'sign/reg3.html', {'info': request.session['info']})
        except:
            return render(request, 'sign/reg3.html')

    def post(self, request):
        username1 = request.session['username']
        usernow = UserProfile.objects.get(username=username1)
        # 接受图片上传逻辑
        reg2tpform = forms.reg2tpForm(request.POST, request.FILES)
        print(reg2tpform.is_valid())
        # 判断是新上传，还是要替换原来老的上传的营业执照
        if reg2tpform.is_valid():
            try:  # 查询是否有记录，如果有就更新照片
                ui = userAuthinfo.objects.get(userid=usernow)
                yyzz = request.FILES.get('yyzz')
                ui.img = yyzz
                ui.save()
                usernow.currentpoint = "ck"  # 表示客户注册后的审批节点
                usernow.save()
                return render(request, 'sign/reg3.html',
                              {"yyzz": ui.img.url,
                               "img1": yyzz
                               })
            except:  # 如果没有记录，就上传照片
                userauthinfoInstance = userAuthinfo()
                yyzz = request.FILES.get('yyzz')
                userauthinfoInstance.img = yyzz
                userauthinfoInstance.userid = usernow
                userauthinfoInstance.save()
                usernow.currentpoint = "ck"  # 表示客户注册后的审批节点
                usernow.save()
                print('ss')
                return render(request, 'sign/reg3.html',
                              {"yyzz": userauthinfoInstance.img.url,
                               "img1": yyzz
                               })

        else:
            return render(request, 'sign/reg3.html', {"reg3Form": reg2tpform})  # form验证信息回显


class MyaccountView(LoginRequiredMixin, View):
    def get(self, request):
        # 获取当前登录的用户信息
        gender = True
        try:
            currentUser = request.user
            if currentUser.is_authenticated:
                if currentUser.gender:
                    gender = 1
                else:
                    gender = 0
                return render(request, 'usercenter/myaccount.html', {'currentuser': currentUser, 'gender': gender})
            else:
                return redirect('/sign/login')
        except Exception as e:
            print(e)
            return render(request, 'sign/login.html')

    def post(self, request):
        username = request.POST.get('username')
        gender = request.POST.get('gender')
        email = request.POST.get('email')

        userinfo = UserProfile.objects.get(username=request.user.username)
        userinfo.username = username
        if gender == '1':
            userinfo.gender = True
        else:
            userinfo.gender = False

        userinfo.email = email
        userinfo.save()

        return redirect('/usercenter/myaccount')


class ModifyPwdView(LoginRequiredMixin, View):
    def get(self, request):
        gender = True
        try:
            currentUser = request.user
            if currentUser.is_authenticated:
                return render(request, 'usercenter/modifypassword.html')
            else:
                return redirect('/sign/login')
        except:
            return redirect('/sign/login')

    def post(self, request):
        mdform = forms.modifypwdform(request.POST)
        if mdform.is_valid():
            pwd = request.POST.get('pwd')
            newpwd1 = request.POST.get('newpwd1')
            newpwd2 = request.POST.get('newpwd2')

            user = authenticate(username=request.user.username, password=pwd)
            if user is not None:
                if newpwd1 == newpwd2:
                    user.password = make_password(newpwd1)
                    user.save()
                    logout(request)
                    # 要一个render
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


class logoutView(LoginRequiredMixin, View):
    def post(self, request):
        v = request.POST.get('logoutin')
        logout(request)
        return redirect('/sign/login')


@login_required
def brands_list(request):
    """
    展示所有的品牌信息
    :param request:
    :return:
    """
    brands_list = brands.objects.filter(isdelete=False).all()
    return render(request, 'products/brands_list.html', {'brands_list': brands_list})


@login_required
def categories_list(request):
    """
    展示所有的分组信息
    :param request:
    :return:
    """
    categories_list = category.objects.filter(Q(isroot=True) & Q(isdelete=False))  # 查找所有的根级分组
    return render(request, 'products/categories_list.html', {'categories_list': categories_list})


def generate_pager_array(page_num, page_count):
    """
    根据相关规则生成分页信息
    :param page_num:
    :param page_count:
    :return:
    """
    window_size = 5
    if page_count <= 7:
        return list(map(lambda x: str(x), range(1, page_num - 1))) + ['{}'.format(page_num)] + list(
            map(lambda x: str(x), range(page_num + 1, page_count + 1)))
    else:
        out = []
        if page_num - window_size <= 2:
            for i in map(lambda x: str(x), list(range(1, window_size + 1))):
                if i == str(page_num):
                    out.append('{}'.format(i))
                else:
                    out.append(i)
            out.append('...')
            out.append(page_count)
        elif page_num - window_size > 2 and page_count - window_size <= page_num:
            out.append('1')
            out.append('...')
            for i in map(lambda x: str(x), list(range(page_count - window_size + 1, page_count))):
                if i == str(page_num):
                    out.append('{}'.format(i))
                else:
                    out.append(i)
            out.append(page_count)
        else:
            out.append('1')
            out.append('...')
            for i in map(lambda x: str(x), list(range(page_num - 2, page_num + 2 + 1))):
                if i == str(page_num):
                    out.append('{}'.format(i))
                else:
                    out.append(i)
            out.append('...')
            out.append(page_count)
        return out


@login_required
def brands_product_list(request, brand_id):
    """
    根据品牌来罗列该品牌的所有商品
    :param request:
    :param brand_id:
    :return:
    """
    # 获取该品牌下所有商品的分类
    categories = category.objects.raw(
        'SELECT * FROM products_category WHERE id in (SELECT DISTINCT categoryid_id FROM products_product WHERE brand_id = %s) AND isdelete=0',
        [brand_id])
    #
    price_range = request.GET.get('price_range')  # 1: 0-20 2: 20-50 3: 50-100 4: 100-200 5: 200以上 0: 无限
    amount_range = request.GET.get('amount_range')  # 1: 0-20 2: 20-50 3: 50-100 4: 100-200 5: 200以上 0：无限
    in_private = request.GET.get('in_private')
    category_id = request.GET.get('category', None)
    if not category_id:
        category_id = None

    brand = get_object_or_404(brands, pk=brand_id)

    result_data_dict = {}  # 视图信息数据字典

    query_set = product.objects.filter(Q(state=0) and Q(isdelete=False))

    query_set = query_set.filter(brand=brand)

    result_data_dict['brand'] = brand

    result_data_dict['brand_categories'] = categories

    for item in categories:
        print(item.id)

    if category_id is not None:
        category_instance = category.objects.get(pk=int(category_id))
        result_data_dict['category'] = category_instance
        query_set = query_set.filter(categoryid=category_instance)

    # 价格查询逻辑
    def price_0_to_20(queryset):
        return queryset.filter(productItems__price__range=[0, 20]).distinct()

    def price_20_to_50(queryset):
        print(1)
        return queryset.filter(productItems__price__range=[20, 50]).distinct()

    def price_50_to_100(queryset):
        return queryset.filter(productItems__price__range=[50, 100]).distinct()

    def price_100_to_200(queryset):
        return queryset.filter(productItems__price__range=[100, 200]).distinct()

    def price_gte_200(queryset):
        return queryset.filter(productItems__price__gte=200).distinct()

    price_query_switch = {
        '1': price_0_to_20,
        '2': price_20_to_50,
        '3': price_50_to_100,
        '4': price_100_to_200,
        '5': price_gte_200,
        '0': lambda x: x
    }

    if price_range is not None:
        if price_range not in ['1', '2', '3', '4', '5']:
            price_range = '0'
        query_set = price_query_switch[price_range](query_set)
        result_data_dict['price_range'] = price_range
    else:
        result_data_dict['price_range'] = '0'

    # 库存查询逻辑
    # TODO:待确认具体的库存逻辑
    '''
    def amount_0_to_20(queryset):
        return queryset.filter(productItems__price__range = [0, 20])

    def amount_20_to_50(queryset):
        return queryset.filter(productItems__price__range = [20, 50])

    def amount_50_to_100(queryset):
        return queryset.filter(productItems__price__range = [50, 100])

    def amount_100_to_200(queryset):
        return queryset.filter(productItems__price__range = [100, 200])

    def amount_gte_200(queryset):
        return queryset.filter(productItems__price__gte = 200)

    amount_query_switch = {
        '1': amount_0_to_20,
        '2': amount_20_to_50,
        '3': amount_50_to_100,
        '4': amount_100_to_200,
        '5': amount_gte_200
    }

    if amount_query_switch is not None:
        if amount_range not in ['1', '2', '3', '4', '5']:
            amount_range = '1'
        query_set = amount_query_switch[price_range](query_set)
    '''

    if request.user.privatearea is not None:  # 如果当前用户不存在私有域
        result_data_dict['has_private_area'] = True
        if in_private is not None:
            result_data_dict['in_private'] = in_private
            if in_private is '1':
                query_set = query_set.filter(privatearea=request.user.privatearea)
            elif in_private is '0':  # 0 则是所有类型，不做任何处理
                query_set = query_set.filter(Q(privatearea=request.user.privatearea) | Q(inprivatearea=False))
            else:
                query_set = query_set.filter(inprivatearea=False)
        else:
            result_data_dict['in_private'] = '0'
    else:
        result_data_dict['has_private_area'] = False

    query_set = query_set.order_by('id')
    # 分页处理
    paginator = Paginator(query_set, 12)
    page = request.GET.get('page')
    products = paginator.get_page(page)

    result_data_dict['products'] = products
    result_data_dict['page_range'] = range(1, products.paginator.num_pages)

    pager_array = generate_pager_array(products.number, products.paginator.num_pages)
    result_data_dict['pager_array'] = pager_array

    return render(request, 'products/brand_product_list.html', result_data_dict)
    pass


@login_required
def category_product_list(request, parent_category_id, child_category_id):
    """
    根据父分组和子分组来罗列出其中的所有商品
    :param request:
    :return:
    """
    price_range = request.GET.get('price_range')  # 1: 0-20 2: 20-50 3: 50-100 4: 100-200 5: 200以上 0: 无限
    amount_range = request.GET.get('amount_range')  # 1: 0-20 2: 20-50 3: 50-100 4: 100-200 5: 200以上 0：无限
    in_private = request.GET.get('in_private')

    result_data_dict = {}  # 视图信息数据字典

    query_set = product.objects.filter(Q(state=0) and Q(isdelete=False))
    category_instance = get_object_or_404(category, pk=child_category_id)  # 获取子分组实例
    parent_category_instance = get_object_or_404(category, pk=parent_category_id)  # 获取父分组实例

    if category_instance.parent.id is not parent_category_id:  # 如果传入的参数父子分组参数不对应，则返回400错误
        return HttpResponseBadRequest()

    query_set = query_set.filter(categoryid=category_instance)

    result_data_dict['root_category'] = parent_category_instance
    result_data_dict['category'] = category_instance

    # 价格查询逻辑
    def price_0_to_20(queryset):
        return queryset.filter(productItems__price__range=[0, 20]).distinct()

    def price_20_to_50(queryset):
        print(1)
        return queryset.filter(productItems__price__range=[20, 50]).distinct()

    def price_50_to_100(queryset):
        return queryset.filter(productItems__price__range=[50, 100]).distinct()

    def price_100_to_200(queryset):
        return queryset.filter(productItems__price__range=[100, 200]).distinct()

    def price_gte_200(queryset):
        return queryset.filter(productItems__price__gte=200).distinct()

    price_query_switch = {
        '1': price_0_to_20,
        '2': price_20_to_50,
        '3': price_50_to_100,
        '4': price_100_to_200,
        '5': price_gte_200,
        '0': lambda x: x
    }

    if price_range is not None:
        if price_range not in ['1', '2', '3', '4', '5']:
            price_range = '0'
        query_set = price_query_switch[price_range](query_set)
        result_data_dict['price_range'] = price_range
    else:
        result_data_dict['price_range'] = '0'

    # 库存查询逻辑
    # TODO:待确认具体的库存逻辑
    '''
    def amount_0_to_20(queryset):
        return queryset.filter(productItems__price__range = [0, 20])

    def amount_20_to_50(queryset):
        return queryset.filter(productItems__price__range = [20, 50])

    def amount_50_to_100(queryset):
        return queryset.filter(productItems__price__range = [50, 100])

    def amount_100_to_200(queryset):
        return queryset.filter(productItems__price__range = [100, 200])

    def amount_gte_200(queryset):
        return queryset.filter(productItems__price__gte = 200)

    amount_query_switch = {
        '1': amount_0_to_20,
        '2': amount_20_to_50,
        '3': amount_50_to_100,
        '4': amount_100_to_200,
        '5': amount_gte_200
    }

    if amount_query_switch is not None:
        if amount_range not in ['1', '2', '3', '4', '5']:
            amount_range = '1'
        query_set = amount_query_switch[price_range](query_set)
    '''

    if request.user.privatearea is not None:  # 如果当前用户不存在私有域
        result_data_dict['has_private_area'] = True
        if in_private is not None:
            result_data_dict['in_private'] = in_private
            if in_private is '1':
                query_set = query_set.filter(privatearea=request.user.privatearea)
            elif in_private is '0':  # 0 则是所有类型，不做任何处理
                query_set = query_set.filter(Q(privatearea=request.user.privatearea) | Q(inprivatearea=False))
            else:
                query_set = query_set.filter(inprivatearea=False)
        else:
            result_data_dict['in_private'] = '0'
    else:
        result_data_dict['has_private_area'] = False

    query_set = query_set.order_by('id')
    # 分页处理
    paginator = Paginator(query_set, 12)
    page = request.GET.get('page')
    products = paginator.get_page(page)

    result_data_dict['products'] = products
    result_data_dict['page_range'] = range(1, products.paginator.num_pages)

    pager_array = generate_pager_array(products.number, products.paginator.num_pages)
    result_data_dict['pager_array'] = pager_array

    return render(request, 'products/category_product_list.html', result_data_dict)


@login_required
def root_category_product_list(request, parent_category_id):
    price_range = request.GET.get('price_range')  # 1: 0-20 2: 20-50 3: 50-100 4: 100-200 5: 200以上 0: 无限
    amount_range = request.GET.get('amount_range')  # 1: 0-20 2: 20-50 3: 50-100 4: 100-200 5: 200以上 0：无限
    in_private = request.GET.get('in_private')

    result_data_dict = {}  # 视图信息数据字典

    query_set = product.objects.filter(Q(state=0) and Q(isdelete=False))
    parent_category_instance = get_object_or_404(category, pk=parent_category_id)  # 获取父分组实例

    query_set = query_set.filter(categoryid__parent=parent_category_instance)

    result_data_dict['root_category'] = parent_category_instance

    # 价格查询逻辑
    def price_0_to_20(queryset):
        return queryset.filter(productItems__price__range=[0, 20]).distinct()

    def price_20_to_50(queryset):
        return queryset.filter(productItems__price__range=[20, 50]).distinct()

    def price_50_to_100(queryset):
        return queryset.filter(productItems__price__range=[50, 100]).distinct()

    def price_100_to_200(queryset):
        return queryset.filter(productItems__price__range=[100, 200]).distinct()

    def price_gte_200(queryset):
        return queryset.filter(productItems__price__gte=200).distinct()

    price_query_switch = {
        '1': price_0_to_20,
        '2': price_20_to_50,
        '3': price_50_to_100,
        '4': price_100_to_200,
        '5': price_gte_200,
        '0': lambda x: x
    }

    if price_range is not None:
        if price_range not in ['1', '2', '3', '4', '5']:
            price_range = '0'
        query_set = price_query_switch[price_range](query_set)
        result_data_dict['price_range'] = price_range
    else:
        result_data_dict['price_range'] = '0'

    # 库存查询逻辑
    # TODO:待确认具体的库存逻辑
    '''
    def amount_0_to_20(queryset):
        return queryset.filter(productItems__price__range = [0, 20])

    def amount_20_to_50(queryset):
        return queryset.filter(productItems__price__range = [20, 50])

    def amount_50_to_100(queryset):
        return queryset.filter(productItems__price__range = [50, 100])

    def amount_100_to_200(queryset):
        return queryset.filter(productItems__price__range = [100, 200])

    def amount_gte_200(queryset):
        return queryset.filter(productItems__price__gte = 200)

    amount_query_switch = {
        '1': amount_0_to_20,
        '2': amount_20_to_50,
        '3': amount_50_to_100,
        '4': amount_100_to_200,
        '5': amount_gte_200
    }

    if amount_query_switch is not None:
        if amount_range not in ['1', '2', '3', '4', '5']:
            amount_range = '1'
        query_set = amount_query_switch[price_range](query_set)
    '''

    if request.user.privatearea is not None:  # 如果当前用户不存在私有域
        result_data_dict['has_private_area'] = True
        if in_private is not None:
            result_data_dict['in_private'] = in_private
            if in_private is '1':
                query_set = query_set.filter(privatearea=request.user.privatearea)
            elif in_private is '0':  # 0 则是所有类型，不做任何处理
                query_set = query_set.filter(Q(privatearea=request.user.privatearea) | Q(inprivatearea=False))
            else:
                query_set = query_set.filter(inprivatearea=False)
        else:
            result_data_dict['in_private'] = '0'
    else:
        result_data_dict['has_private_area'] = False

    query_set = query_set.order_by('id')
    # 分页处理
    paginator = Paginator(query_set, 12)
    page = request.GET.get('page')
    products = paginator.get_page(page)

    result_data_dict['products'] = products
    result_data_dict['page_range'] = range(1, products.paginator.num_pages)

    pager_array = generate_pager_array(products.number, products.paginator.num_pages)
    result_data_dict['pager_array'] = pager_array

    return render(request, 'products/root_category_product_list.html', result_data_dict)


@login_required
def search_supplier(request):
    """
    商家搜索逻辑
    :param request:
    :return:
    """
    query_content = request.GET.get('q')

    result_data_dict = {}  # 视图信息数据字典

    query_set = supplier.objects

    if query_content is not None:
        query_set = query_set.filter(suppliername__contains=query_content)
        result_data_dict['search_query'] = query_content
    else:
        result_data_dict['search_query'] = ''

    query_set = query_set.order_by('id')

    # 分页处理
    paginator = Paginator(query_set, 6)
    page = request.GET.get('page')
    suppliers = paginator.get_page(page)

    result_data_dict['suppliers'] = suppliers
    result_data_dict['page_range'] = range(1, suppliers.paginator.num_pages)

    pager_array = generate_pager_array(suppliers.number, suppliers.paginator.num_pages)
    result_data_dict['pager_array'] = pager_array

    return render(request, 'search/supplier_search_result_list.html', result_data_dict)


@login_required
def search_products(request):
    """
    产品全局搜索的代码逻辑
    :param request:
    :return:
    """
    price_range = request.GET.get('price_range')  # 1: 0-20 2: 20-50 3: 50-100 4: 100-200 5: 200以上 0: 无限
    amount_range = request.GET.get('amount_range')  # 1: 0-20 2: 20-50 3: 50-100 4: 100-200 5: 200以上 0：无限
    in_private = request.GET.get('in_private')
    query_content = request.GET.get('q')

    result_data_dict = {}  # 视图信息数据字典

    query_set = product.objects.filter(Q(state=0) and Q(isdelete=False))

    if query_content is not None:
        query_set = query_set.filter(name__contains=query_content)
        result_data_dict['search_query'] = query_content
    else:
        result_data_dict['search_query'] = ''

    # 价格查询逻辑
    def price_0_to_20(queryset):
        return queryset.filter(productItems__price__range=[0, 20]).distinct()

    def price_20_to_50(queryset):
        print(1)
        return queryset.filter(productItems__price__range=[20, 50]).distinct()

    def price_50_to_100(queryset):
        return queryset.filter(productItems__price__range=[50, 100]).distinct()

    def price_100_to_200(queryset):
        return queryset.filter(productItems__price__range=[100, 200]).distinct()

    def price_gte_200(queryset):
        return queryset.filter(productItems__price__gte=200).distinct()

    price_query_switch = {
        '1': price_0_to_20,
        '2': price_20_to_50,
        '3': price_50_to_100,
        '4': price_100_to_200,
        '5': price_gte_200,
        '0': lambda x: x
    }

    if price_range is not None:
        if price_range not in ['1', '2', '3', '4', '5']:
            price_range = '0'
        query_set = price_query_switch[price_range](query_set)
        result_data_dict['price_range'] = price_range
    else:
        result_data_dict['price_range'] = '0'

    # 库存查询逻辑
    # TODO:待确认具体的库存逻辑
    '''
    def amount_0_to_20(queryset):
        return queryset.filter(productItems__price__range = [0, 20])

    def amount_20_to_50(queryset):
        return queryset.filter(productItems__price__range = [20, 50])

    def amount_50_to_100(queryset):
        return queryset.filter(productItems__price__range = [50, 100])

    def amount_100_to_200(queryset):
        return queryset.filter(productItems__price__range = [100, 200])

    def amount_gte_200(queryset):
        return queryset.filter(productItems__price__gte = 200)

    amount_query_switch = {
        '1': amount_0_to_20,
        '2': amount_20_to_50,
        '3': amount_50_to_100,
        '4': amount_100_to_200,
        '5': amount_gte_200
    }

    if amount_query_switch is not None:
        if amount_range not in ['1', '2', '3', '4', '5']:
            amount_range = '1'
        query_set = amount_query_switch[price_range](query_set)
    '''

    if request.user.privatearea is not None:  # 如果当前用户不存在私有域
        result_data_dict['has_private_area'] = True
        if in_private is not None:
            result_data_dict['in_private'] = in_private
            if in_private is '1':
                query_set = query_set.filter(privatearea=request.user.privatearea)
            elif in_private is '0':  # 0 则是所有类型，不做任何处理
                query_set = query_set.filter(Q(privatearea=request.user.privatearea) | Q(inprivatearea=False))
            else:
                query_set = query_set.filter(inprivatearea=False)
        else:
            result_data_dict['in_private'] = '0'
    else:
        result_data_dict['has_private_area'] = False

    query_set = query_set.order_by('id')

    # 分页处理
    paginator = Paginator(query_set, 12)
    page = request.GET.get('page')
    products = paginator.get_page(page)

    result_data_dict['products'] = products
    result_data_dict['page_range'] = range(1, products.paginator.num_pages)

    pager_array = generate_pager_array(products.number, products.paginator.num_pages)
    result_data_dict['pager_array'] = pager_array

    return render(request, 'search/product_search_result.html', result_data_dict)


class msgCenterView(View):
    @method_decorator(login_required)
    def get(self, request):
        query_set = siteMessge.objects.all()
        query_set = query_set.filter(~Q(fromuser=1))

        paginator = Paginator(query_set, 12)
        page = request.GET.get('page')
        msgs = paginator.get_page(page)

        result_data_dict = {}
        result_data_dict['currentpage'] = 'msgcenter'
        result_data_dict['msgs'] = msgs
        result_data_dict['page_range'] = range(1, msgs.paginator.num_pages)

        pager_array = generate_pager_array(msgs.number, msgs.paginator.num_pages)
        result_data_dict['pager_array'] = pager_array

        return render(request, 'inforcenter/msgcenter.html', result_data_dict)


class msgdetailView(View):
    @method_decorator(login_required)
    def get(self, request):
        msgid = request.GET.get('m')
        msgobj = siteMessge.objects.get(pk=int(msgid))
        msgobj.hasread = True
        msgobj.save()
        print(msgobj.content)
        currentpage = 'msgdetail'
        return render(request, 'inforcenter/msgdetail.html',
                      {'msgobj': msgobj,
                       'currentpage': currentpage
                       }
                      )


# TODO: 系统管理员发的系统消息
class sysinfoView(View):
    @method_decorator(login_required)
    def get(self, request):
        query_set = siteMessge.objects.all()
        query_set = query_set.filter(fromuser=1)

        paginator = Paginator(query_set, 5)
        page = request.GET.get('page')
        msgs = paginator.get_page(page)

        result_data_dict = {}
        result_data_dict['currentpage'] = 'sysinfo'
        result_data_dict['msgs'] = msgs
        result_data_dict['page_range'] = range(1, msgs.paginator.num_pages)

        pager_array = generate_pager_array(msgs.number, msgs.paginator.num_pages)
        result_data_dict['pager_array'] = pager_array

        return render(request, 'usercenter/sysinfo.html', result_data_dict)


class sysinfodetailView(View):
    @method_decorator(login_required)
    def get(self, request):
        msgid = request.GET.get('m')
        msgobj = siteMessge.objects.get(pk=int(msgid))
        msgobj.hasread = True
        msgobj.save()
        currentpage = 'sysinfodetail'
        return render(request, 'usercenter/sysinfodetail.html',
                      {
                          'msgobj': msgobj,
                          'currentpage':currentpage
                      }
                      )


class findpwdView(View):
    def get(self, request):
        return render(request, 'sign/findpwd.html')
    def post(self,request):
        fndform = forms.findpwdform(request.POST)
        if fndform.is_valid():
            mobile = request.POST.get("mobile")
            checkcode = request.POST.get("checkcode")
            pwd1 = request.POST.get("pwd1")
            pwd2 = request.POST.get("pwd2")

            user = None

            try:
                user = UserProfile.objects.get(mobile=mobile)
            except  Exception as e:
                user= None

            if user is not None:
                if pwd1 == pwd2:
                    user.password = make_password(pwd1)
                    user.save()
                    resinfo="密码修改成功"
                    return render(request,
                                  'sign/findpwd.html',
                                  {'resinfo': resinfo})
                else:
                    errormessge1 = "两次输入的密码不一致"
                    return render(request,
                                  'sign/findpwd.html',
                                  {'errormesg1': errormessge1})
            else:
                # 手机号不存在
                errormessge = "手机号不存在"
                return render(request,
                              'sign/findpwd.html',
                              {'errormesg': errormessge})
        else:
            return render(request,
                          'sign/findpwd.html',
                          {'fndform': fndform})




def delete_from_cart(request, product_id):
    """
    删除方案车中的方案
    :param request:
    :return:
    """
    if request.method == "DELETE":
        temp = {
            'product_id': product_id,
        }
        if temp in request.session['cart']:
            request.session['cart'].remove(temp)
            request.session.modified = True
            return HttpResponse(json.dumps({'result': 'ok'}), content_type="application/json", status='200')
        else:
            return HttpResponse(json.dumps({'result': 'error', 'message': 'not found'}),
                                content_type="application/json", status='404')


class CartView(View):
    """
    方案车视图方法
    """

    def get(self, request):
        """
        获取方案车的所有列表
        :param request:
        :return:
        """
        result = []
        if request.session.get('cart', False):
            for cart_item in request.session.get('cart'):
                print(cart_item)
                product_instance = product.objects.get(pk=cart_item['product_id'])
                result.append({
                    'productName': product_instance.name,
                    'mainImage': product_instance.images.first().productimage.url,
                    'productId': cart_item['product_id'],
                })
            return HttpResponse(json.dumps(result), content_type="application/json", status='200')
        else:
            return HttpResponse(json.dumps(result), content_type="application/json", status='200')

    def post(self, request):
        """
        在方案车中加入相关商品,使用post提交，主要参数为商品主id和sku id
        :param request:
        :return:
        """
        product_id = int(request.POST.get('productId'))

        product_instance = product.objects.get(pk=product_id)

        print(product_id)

        if product_instance is None:
            return HttpResponse(json.dumps({'result': 'error', 'message': 'product not existed'}),
                                content_type="application/json", status="404")

        temp = {
            'product_id': product_id
        }
        if request.session.get('cart', False):
            existed_products = request.session.get('cart')
            if temp in existed_products:  # 如果已经存在于方案车，则返回错误信息
                return HttpResponse(json.dumps({'result': 'error', 'message': 'has existed'}),
                                    content_type="application/json", status="400")

            existed_products.append(
                {
                    'product_id': product_id
                }
            )
            request.session['cart'] = existed_products
        else:
            request.session['cart'] = [
                {
                    'product_id': product_id
                }
            ]

        return HttpResponse(json.dumps({'result': 'ok'}), content_type="application/json", status="200")


class protocolView(View):
    def get(self, request):
        return render(request, 'others/protocol.html')


def product_details(request, product_id):
    """
    商品详情信息
    :param request:
    :param product_id: 商品id
    :return:
    """
    result_dict = {}
    product_instance = get_object_or_404(product, pk=product_id)

    def default(obj):
        if isinstance(obj, Decimal):
            return str(obj)
        raise TypeError("Object of type '%s' is not JSON serializable" % type(obj).__name__)

    product_item_list_query_set = productItem.objects.filter(product=product_instance).prefetch_related('images')
    product_item_list = []
    for record in product_item_list_query_set:
        temp_dict = {}
        temp_dict['id'] = record.id
        temp_dict['attributes'] = record.attributes
        temp_dict['price'] = record.price
        temp_dict['image'] = record.images.first().productimage.url
        product_item_list.append(temp_dict)
    print(product_item_list)
    result_dict["product_items_json"] = json.dumps(product_item_list, default=default)

    # 根据所有商品sku计算商品的价格区间范围
    product_items = product_instance.productItems.order_by("price").all()
    result_dict["start_price"] = product_items.first().price
    result_dict["end_price"] = product_items.last().price
    #

    result_dict["main_images"] = product_instance.images.all()

    result_dict["supplier_name"] = product_instance.belongs.supplier.suppliername

    result_dict["product"] = product_instance

    # 开始统计所有的属性和对应的方法
    # TODO: 后台改进，将各个属性的具体值存入数据库防止重复计算
    attribute_values_dic = {}
    product_items = product_instance.productItems.all()
    for attribute_name in product_instance.attributes:
        for product_item in product_items:
            if attribute_name not in attribute_values_dic:
                # 如果字典中不包含此key，则新建相关数据
                attribute_values_dic[attribute_name] = [product_item.attributes[attribute_name]]
            else:
                if product_item.attributes[attribute_name] not in attribute_values_dic[attribute_name]:
                    attribute_values_dic[attribute_name].append(product_item.attributes[attribute_name])

    result_dict["attribute_values"] = attribute_values_dic

    return render(request, "products/details.html", result_dict)


def export_ppt(request):
    """
    生成PPT并且提供下载
    :param request:
    :return:
    """
    if request.session.get('cart', False):
        id_list = []
        ppt_path = 'ppt/{0}/{1}.pptx'.format(request.user.id, datetime.datetime.now().strftime('%Y%m%d%H%M%S%f'))
        ppt_absolute_path = os.path.join(settings.MEDIA_ROOT, ppt_path)
        for cart_item in request.session.get('cart'):
            id_list.append(cart_item['product_id'])
        generate_ppt(product.objects.filter(pk__in=id_list), ppt_absolute_path)
        print(ppt_path)
        return HttpResponse(json.dumps({'result': 'ok', 'file_url': '/media/{}'.format(ppt_path)}),
                            content_type="application/json", status="200")
        # 开始进行ppt生成操作
    else:
        return HttpResponse(json.dumps({'result': 'error', 'message': 'cart is empty'}),
                            content_type="application/json", status="400")


@login_required
def one_send_product_list(request):
    """
    根据品牌来罗列该品牌的所有商品
    :param request:
    :param brand_id:
    :return:
    """
    # 获取该品牌下所有商品的分类
    categories = category.objects.raw(
        'SELECT * FROM products_category WHERE id in (SELECT DISTINCT categoryid_id FROM products_product WHERE yijiandaifa = 1)')
    #
    price_range = request.GET.get('price_range')  # 1: 0-20 2: 20-50 3: 50-100 4: 100-200 5: 200以上 0: 无限
    amount_range = request.GET.get('amount_range')  # 1: 0-20 2: 20-50 3: 50-100 4: 100-200 5: 200以上 0：无限
    in_private = request.GET.get('in_private')
    category_id = request.GET.get('category', None)
    if not category_id:
        category_id = None

    result_data_dict = {}  # 视图信息数据字典

    query_set = product.objects.filter(Q(state=0) and Q(isdelete=False))

    query_set = query_set.filter(yijiandaifa=True)

    result_data_dict['one_send_categories'] = categories

    for item in categories:
        print(item.id)

    if category_id is not None:
        category_instance = category.objects.get(pk=int(category_id))
        result_data_dict['category'] = category_instance
        query_set = query_set.filter(categoryid=category_instance)

    # 价格查询逻辑
    def price_0_to_20(queryset):
        return queryset.filter(productItems__price__range=[0, 20]).distinct()

    def price_20_to_50(queryset):
        print(1)
        return queryset.filter(productItems__price__range=[20, 50]).distinct()

    def price_50_to_100(queryset):
        return queryset.filter(productItems__price__range=[50, 100]).distinct()

    def price_100_to_200(queryset):
        return queryset.filter(productItems__price__range=[100, 200]).distinct()

    def price_gte_200(queryset):
        return queryset.filter(productItems__price__gte=200).distinct()

    price_query_switch = {
        '1': price_0_to_20,
        '2': price_20_to_50,
        '3': price_50_to_100,
        '4': price_100_to_200,
        '5': price_gte_200,
        '0': lambda x: x
    }

    if price_range is not None:
        if price_range not in ['1', '2', '3', '4', '5']:
            price_range = '0'
        query_set = price_query_switch[price_range](query_set)
        result_data_dict['price_range'] = price_range
    else:
        result_data_dict['price_range'] = '0'

    # 库存查询逻辑
    # TODO:待确认具体的库存逻辑
    '''
    def amount_0_to_20(queryset):
        return queryset.filter(productItems__price__range = [0, 20])

    def amount_20_to_50(queryset):
        return queryset.filter(productItems__price__range = [20, 50])

    def amount_50_to_100(queryset):
        return queryset.filter(productItems__price__range = [50, 100])

    def amount_100_to_200(queryset):
        return queryset.filter(productItems__price__range = [100, 200])

    def amount_gte_200(queryset):
        return queryset.filter(productItems__price__gte = 200)

    amount_query_switch = {
        '1': amount_0_to_20,
        '2': amount_20_to_50,
        '3': amount_50_to_100,
        '4': amount_100_to_200,
        '5': amount_gte_200
    }

    if amount_query_switch is not None:
        if amount_range not in ['1', '2', '3', '4', '5']:
            amount_range = '1'
        query_set = amount_query_switch[price_range](query_set)
    '''

    if request.user.privatearea is not None:  # 如果当前用户不存在私有域
        result_data_dict['has_private_area'] = True
        if in_private is not None:
            result_data_dict['in_private'] = in_private
            if in_private is '1':
                query_set = query_set.filter(privatearea=request.user.privatearea)
            elif in_private is '0':  # 0 则是所有类型，不做任何处理
                query_set = query_set.filter(Q(privatearea=request.user.privatearea) | Q(inprivatearea=False))
            else:
                query_set = query_set.filter(inprivatearea=False)
        else:
            result_data_dict['in_private'] = '0'
    else:
        result_data_dict['has_private_area'] = False

    query_set = query_set.order_by('id')
    # 分页处理
    paginator = Paginator(query_set, 12)
    page = request.GET.get('page')
    products = paginator.get_page(page)

    result_data_dict['products'] = products
    result_data_dict['page_range'] = range(1, products.paginator.num_pages)

    pager_array = generate_pager_array(products.number, products.paginator.num_pages)
    result_data_dict['pager_array'] = pager_array

    return render(request, 'products/one_send_product_list.html', result_data_dict)


def new_private_supplier(request):
    # if request.user.privatearea is None:
    #    return HttpResponse(status=403) # 如果本身不具有私有域，则抛出403错误
    """
    创建新的私有域供应商
    :param request:
    :return:
    """
    # 开始判断是否已经达到私有域供应商的上限
    privatearea = request.user.privatearea
    if privatearea.accountlimit <= UserProfile.objects.filter(Q(privatearea_id= privatearea.id) and Q(type='supplier')).count():
        messages.add_message(request, messages.ERROR, '您的供应商账号数量已达上限')
        return redirect('/usercenter/privatearea/suppliers')
    else:
        return render(request, 'usercenter/new_supplier_in_private_area.html')


def edit_private_supplier(request, supplier_id):
    """
    编辑私有域供应商的基本信息
    :param request:
    :param supplier_id:
    :return:
    """
    supplier = get_object_or_404(UserProfile, pk=supplier_id)
    if supplier.privatearea.id != request.user.privatearea.id:
        return HttpResponseNotFound()
    if request.method == 'POST':
        method = request.POST.get('_method', None)
        if method == 'PUT':
            supplier_info = supplier.supplier
            supplier_info.suppliername = request.POST['supplier_name']
            supplier_info.tel = request.POST['tel']
            supplier_info.qq = request.POST['qq']
            supplier_info.save()
            messages.add_message(request, messages.SUCCESS, '基本信息修改成功')
            return redirect('/usercenter/privatearea/suppliers')
        else:
            return redirect('/usercenter/privatearea/suppliers')
    elif request.method == 'GET':
        supplier = get_object_or_404(UserProfile, pk=supplier_id)
        return render(request, "usercenter/edit_private_supplier.html",
                      {'supplier_info': supplier.supplier})


class PrivateSupplier(View):
    def get(self, request):
        query_set = UserProfile.objects.filter(type="supplier")
        query_set = query_set.filter(Q(privatearea=request.user.privatearea) and Q(inprivatearea=True))

        result_data_dict = {}

        # 分页处理
        paginator = Paginator(query_set, 12)
        page = request.GET.get('page')
        suppliers = paginator.get_page(page)

        result_data_dict['suppliers'] = suppliers
        result_data_dict['page_range'] = range(1, suppliers.paginator.num_pages)

        pager_array = generate_pager_array(suppliers.number, suppliers.paginator.num_pages)
        result_data_dict['pager_array'] = pager_array

        return render(request, 'usercenter/private_area_supplier_list.html', result_data_dict)

    def post(self, request):
        """
        创建新的私有域供应商
        :param request:
        :return:
        """
        form = forms.PrivateAreaSupplierForm(request.POST)
        print(form)
        if form.is_valid():
            user = UserProfile.objects.create_user(username=form.cleaned_data['username'],
                                                   password=form.cleaned_data['password'])
            user.type = 'supplier'
            user.privatearea = request.user.privatearea
            user.authStatus = True
            user.inprivatearea = True
            user.save()

            supplier_info = supplier(suppliername=form.cleaned_data['supplier_name'], tel=form.cleaned_data['tel'],
                                     qq=form.cleaned_data['qq'], email=form.cleaned_data['email'], userid=user)
            supplier_info.save()
            messages.add_message(request, messages.SUCCESS, '已成功创建私有供应商')

            return redirect('/usercenter/privatearea/suppliers')
        else:
            return render(request, 'usercenter/new_supplier_in_private_area.html')
