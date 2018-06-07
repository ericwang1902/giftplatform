from django import forms
from apps.users.models import UserProfile

class regForm(forms.Form):
    username =forms.CharField(required=True,error_messages={'required':u'用户名不能为空'})
    mobile =forms.CharField(required=True,error_messages={'required':u'手机号不能为空'})
    checkcode =forms.CharField(required=True,error_messages={'required':u'验证码不能为空'})
    email = forms.CharField(required=True,error_messages={'required':u'邮箱不能为空'})
    pwd1 =forms.CharField(required=True,error_messages={'required':u'密码不能为空'})
    pwd2 = forms.CharField(required=True,error_messages={'required':u'请重复输入密码'})
    vehicle=forms.BooleanField(required=True,error_messages={'required':u'请确认是否同意使用协议'})
   # usertype = forms.CharField(required=True)

class reg2tpForm(forms.Form):
    pp=forms.CharField(required=True,error_messages={'required':u'sss'})
    yyzz =forms.ImageField(required=True,error_messages={'required':u"请上传营业执照照片"})

class modifypwdform(forms.Form):
    pwd =forms.CharField(required=True,error_messages={'required':u'请输入密码'})
    newpwd1 = forms.CharField(required=True,error_messages={'required':u'请输入新密码'})
    newpwd2 = forms.CharField(required=True,error_messages={'required':u'请重复输入密码'})

class loginform(forms.Form):
    username = forms.CharField(required=True, error_messages={'required': u'用户名或密码不能为空'})
    password = forms.CharField(required=True, error_messages={'required': u'用户名或密码不能为空'})


class PrivateAreaSupplierForm(forms.Form):
    """
    创建私有域供应商的form
    """
    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            UserProfile.objects.get(username__iexact=username)
        except UserProfile.DoesNotExist:
            return username
        raise forms.ValidationError("用户名已被使用。")

    username = forms.CharField(label="用户名", required=True, error_messages={"required": u"用户名不能为空"}) # 用户名
    password = forms.CharField(required=True)
    supplier_name = forms.CharField(label="供应商店铺名", required=True)
    tel = forms.CharField(required=True, label="联系电话")
    qq = forms.CharField(label="QQ", required=False)
    email = forms.CharField(label="Email", required=False)

class findpwdform(forms.Form):
    mobile = forms.CharField(label="手机号",required=True,error_messages={'required':u'手机号不能为空'})
    checkcode = forms.CharField(required=True, error_messages={'required': u'验证码不能为空'})
    pwd1 = forms.CharField(required=True, error_messages={'required': u'密码不能为空'})
    pwd2 = forms.CharField(required=True, error_messages={'required': u'请重复输入密码'})