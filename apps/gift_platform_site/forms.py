from django import forms

class regForm(forms.Form):
    username =forms.CharField(required=True,error_messages={'required':u'用户名不能为空'})
    mobile =forms.CharField(required=True,error_messages={'required':u'手机号不能为空'})
    checkcode =forms.CharField(required=True,error_messages={'required':u'验证码不能为空'})
    email = forms.CharField(required=True,error_messages={'required':u'邮箱不能为空'})
    pwd1 =forms.CharField(required=True,error_messages={'required':u'密码不能为空'})
    pwd2 = forms.CharField(required=True,error_messages={'required':u'请重复输入密码'})
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