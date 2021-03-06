from django import forms
from apps.users.models import UserProfile
from .models import Invitation
from captcha.fields import CaptchaField

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

    def clean_tel(self):
        tel = self.cleaned_data['tel']
        if UserProfile.objects.filter(mobile__iexact=tel).count() == 0:
            return tel
        raise forms.ValidationError("手机号码已被使用。")

    username = forms.CharField(label="用户名", required=True, error_messages={"required": u"用户名不能为空"}) # 用户名
    password = forms.CharField(required=True)
    supplier_name = forms.CharField(label="供应商店铺名", required=True)
    tel = forms.CharField(required=True, label="联系电话")
    qq = forms.CharField(label="QQ", required=False)
    email = forms.CharField(label="Email", required=False)
    contacts = forms.CharField(label="联系人", required=False)


class findpwdform(forms.Form):
    mobile = forms.CharField(label="手机号",required=True,error_messages={'required':u'手机号不能为空'})
    checkcode = forms.CharField(required=True, error_messages={'required': u'验证码不能为空'})
    pwd1 = forms.CharField(required=True, error_messages={'required': u'密码不能为空'})
    pwd2 = forms.CharField(required=True, error_messages={'required': u'请重复输入密码'})


class InvitationForm(forms.Form):
    """
    邀请试用表单
    """
    name = forms.CharField(label="姓名", required=True, error_messages={"required": u"姓名不能为空"})
    job_position = forms.CharField(label="职位", required=True, error_messages={"required": u"职位不能为空"})
    company_name = forms.CharField(label="公司", required=True, error_messages={"required": u"公司不能为空"})
    tel = forms.CharField(label="联系电话", required=True)
    email = forms.CharField(label="Email", required=False)
    captcha = CaptchaField()


