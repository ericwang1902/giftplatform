from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate,login
from django.views import View
from django.contrib.auth.backends import ModelBackend
from apps.users.models import UserProfile,supplier
from apps.products.models import product,brands,category
from django.db.models import Q
from django.contrib.auth.hashers import make_password
from . import forms
from apps.users.models import userAuthinfo
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.core.paginator import Paginator
from django.http import HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

def home(request):
    """
    home界面，无任何模板，只是用来判断是否已经登录，如果登录则跳转至home/index，否则则跳转至登录界面
    :param request:
    :return:
    """
    pass

class IndexView(LoginRequiredMixin, View):
    def get(self,request):
        products = product.objects.filter(status=0)[0:16]
        currentuser = request.user
        return render(request, "home/index.html", { "products": products,"currentuser":currentuser})

#支持手机号或者用户名登陆
class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            print(username)
            print(password)
            user = UserProfile.objects.get(Q(username=username)|Q(mobile=username))
            print( user.check_password(password))
            if user.check_password(password) :
                return user
        except  Exception as e:
            return None


class LoginView(View):
    def get(self, request):
        return render(request, "sign/login.html")

    def post(self, request):
        loginForm = forms.loginform(request.POST)
        if loginForm.is_valid():
            user = authenticate(username=request.POST['username'], password=request.POST['password'])
            print(user)
            if user is not None and user.currentpoint!='ck':
                # 如果用户不为空，则继续检查该账户类型，只能由商户登录进入
                print(user.type)
                if user.authStatus ==True:
                    if user.type == 'giftcompany':
                        login(request, user)
                        print("登陆成功")
                        return redirect('/home')
                    else:
                        return render(request, 'sign/login.html', {
                            'error_message': "用户名或者密码错误"
                        })
                else:
                    if user.type == 'giftcompany':
                        login(request, user)
                        request.session["username"] = user.username
                        request.session['info']="未通过认证，请重新上传"
                        return redirect('/sign/reg3')
                    else:
                        return render(request, 'sign/login.html', {
                            'error_message': "用户名或者密码错误"
                        })


            elif user.currentpoint=='ck':
                return render(request, 'sign/login.html', {
                    'sh_message': "请等待审核通过后再进行登录"
                })

        else:
            return render(request, 'sign/login.html', {
                'loginform': loginForm
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
                usertype=request.GET.get("type")
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
        info = request.session['info']
        return render(request,'sign/reg3.html',{'info':info})
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
                usernow.currentpoint = "ck"  # 表示客户注册后的审批节点
                usernow.save()
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
                    usernow.currentpoint = "ck"  # 表示客户注册后的审批节点
                    usernow.save()
                    print('ss')
                    return render(request, 'sign/reg3.html',
                                  {"yyzz": userauthinfoInstance.img.url,
                                   "img1":yyzz
                                   })

        else:
            return render(request, 'sign/reg3.html', {"reg3Form": reg2tpform})  # form验证信息回显





class MyaccountView(LoginRequiredMixin, View):
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
        except Exception as e:
            print(e)
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


class ModifyPwdView(LoginRequiredMixin, View):
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


class logoutView(LoginRequiredMixin, View):
    def post(self,request):
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
    brands_list = brands.objects.all()
    return render(request, 'products/brands_list.html', { 'brands_list': brands_list })

@login_required
def categories_list(request):
    """
    展示所有的分组信息
    :param request:
    :return:
    """
    categories_list = category.objects.filter(isroot = True) # 查找所有的根级分组
    return render(request, 'products/categories_list.html', { 'categories_list': categories_list  })

def generate_pager_array(page_num, page_count):
    """
    根据相关规则生成分页信息
    :param page_num:
    :param page_count:
    :return:
    """
    window_size = 5
    if page_count <= 7:
        return list(map(lambda x: str(x), range(1, page_num - 1))) + ['{}'.format(page_num)] + list(map(lambda x: str(x), range(page_num + 1, page_count + 1)))
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
def category_product_list(request, parent_category_id, child_category_id):
    """
    根据父分组和子分组来罗列出其中的所有商品
    :param request:
    :return:
    """
    price_range = request.GET.get('price_range') # 1: 0-20 2: 20-50 3: 50-100 4: 100-200 5: 200以上 0: 无限
    amount_range = request.GET.get('amount_range') # 1: 0-20 2: 20-50 3: 50-100 4: 100-200 5: 200以上 0：无限
    in_private = request.GET.get('in_private')

    result_data_dict = {} # 视图信息数据字典

    query_set = product.objects
    category_instance = get_object_or_404(category, pk=child_category_id) # 获取子分组实例
    parent_category_instance = get_object_or_404(category, pk=parent_category_id) # 获取父分组实例

    if category_instance.parent.id is not parent_category_id: # 如果传入的参数父子分组参数不对应，则返回400错误
        return HttpResponseBadRequest()

    query_set = query_set.filter(categoryid = category_instance)

    result_data_dict['root_category'] = parent_category_instance
    result_data_dict['category'] = category_instance


    # 价格查询逻辑
    def price_0_to_20(queryset):
        return queryset.filter(productItems__price__range = [0, 20]).distinct()

    def price_20_to_50(queryset):
        print(1)
        return queryset.filter(productItems__price__range = [20, 50]).distinct()

    def price_50_to_100(queryset):
        return queryset.filter(productItems__price__range = [50, 100]).distinct()

    def price_100_to_200(queryset):
        return queryset.filter(productItems__price__range = [100, 200]).distinct()

    def price_gte_200(queryset):
        return queryset.filter(productItems__price__gte = 200).distinct()

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

    if request.user.privatearea is not None: # 如果当前用户不存在私有域
        result_data_dict['has_private_area'] = True
        if in_private is not None:
            result_data_dict['in_private'] = in_private
            if in_private is '1':
                query_set = query_set.filter(privatearea = request.user.privatearea)
            elif in_private is '0': # 0 则是所有类型，不做任何处理
                query_set = query_set.filter(Q(privatearea = request.user.privatearea) | Q(inprivatearea=False))
            else:
                query_set = query_set.filter(inprivatearea = False)
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
    price_range = request.GET.get('price_range') # 1: 0-20 2: 20-50 3: 50-100 4: 100-200 5: 200以上 0: 无限
    amount_range = request.GET.get('amount_range') # 1: 0-20 2: 20-50 3: 50-100 4: 100-200 5: 200以上 0：无限
    in_private = request.GET.get('in_private')

    result_data_dict = {} # 视图信息数据字典

    query_set = product.objects
    parent_category_instance = get_object_or_404(category, pk=parent_category_id) # 获取父分组实例

    query_set = query_set.filter(categoryid__parent = parent_category_instance)

    result_data_dict['root_category'] = parent_category_instance

    # 价格查询逻辑
    def price_0_to_20(queryset):
        return queryset.filter(productItems__price__range = [0, 20]).distinct()

    def price_20_to_50(queryset):
        return queryset.filter(productItems__price__range = [20, 50]).distinct()

    def price_50_to_100(queryset):
        return queryset.filter(productItems__price__range = [50, 100]).distinct()

    def price_100_to_200(queryset):
        return queryset.filter(productItems__price__range = [100, 200]).distinct()

    def price_gte_200(queryset):
        return queryset.filter(productItems__price__gte = 200).distinct()

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

    if request.user.privatearea is not None: # 如果当前用户不存在私有域
        result_data_dict['has_private_area'] = True
        if in_private is not None:
            result_data_dict['in_private'] = in_private
            if in_private is '1':
                query_set = query_set.filter(privatearea = request.user.privatearea)
            elif in_private is '0': # 0 则是所有类型，不做任何处理
                query_set = query_set.filter(Q(privatearea = request.user.privatearea) | Q(inprivatearea=False))
            else:
                query_set = query_set.filter(inprivatearea = False)
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

    result_data_dict = {} # 视图信息数据字典

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
    price_range = request.GET.get('price_range') # 1: 0-20 2: 20-50 3: 50-100 4: 100-200 5: 200以上 0: 无限
    amount_range = request.GET.get('amount_range') # 1: 0-20 2: 20-50 3: 50-100 4: 100-200 5: 200以上 0：无限
    in_private = request.GET.get('in_private')
    query_content = request.GET.get('q')

    result_data_dict = {} # 视图信息数据字典

    query_set = product.objects

    if query_content is not None:
        query_set = query_set.filter(name__contains=query_content)
        result_data_dict['search_query'] = query_content
    else:
        result_data_dict['search_query'] = ''


    # 价格查询逻辑
    def price_0_to_20(queryset):
        return queryset.filter(productItems__price__range = [0, 20]).distinct()

    def price_20_to_50(queryset):
        print(1)
        return queryset.filter(productItems__price__range = [20, 50]).distinct()

    def price_50_to_100(queryset):
        return queryset.filter(productItems__price__range = [50, 100]).distinct()

    def price_100_to_200(queryset):
        return queryset.filter(productItems__price__range = [100, 200]).distinct()

    def price_gte_200(queryset):
        return queryset.filter(productItems__price__gte = 200).distinct()

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

    if request.user.privatearea is not None: # 如果当前用户不存在私有域
        result_data_dict['has_private_area'] = True
        if in_private is not None:
            result_data_dict['in_private'] = in_private
            if in_private is '1':
                query_set = query_set.filter(privatearea = request.user.privatearea)
            elif in_private is '0': # 0 则是所有类型，不做任何处理
                query_set = query_set.filter(Q(privatearea = request.user.privatearea) | Q(inprivatearea=False))
            else:
                query_set = query_set.filter(inprivatearea = False)
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
    def get(self,request):
        try:
            currentUser = request.user
            if currentUser.is_authenticated:
                return render(request, 'inforcenter/msgcenter.html')
            else:
                return redirect('/sign/login')
        except:
            return render(request, 'sign/login.html')

class sysinfoView(View):
    def get(self,request):
        return  render(request,'usercenter/sysinfo.html')