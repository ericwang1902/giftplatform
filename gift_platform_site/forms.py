from django import forms

class regForm(forms.Form):
    username =forms.CharField(required=True)
    mobile =forms.CharField(required=True)
    checkcode =forms.CharField(required=True)
    email = forms.CharField(required=True)
    password =forms.CharField(required=True)
    password2 = forms.CharField(required=True)
    usertype = forms.CharField(required=True)