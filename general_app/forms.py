from django import forms
from .models import User_Detail, CertificateFile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class User_DetailForm(forms.ModelForm):
    class Meta:
        model = User_Detail
        fields = ('address', 'province', 'ministry', 'code', 'cal_date', 'password')
        widgets = {
            'address': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'ที่อยู่', 'rows': '1'}),
            'province': forms.Select(attrs={'class': 'form-control', 'placeholder': 'ขอนแก่น','required': 'true'}),
            'ministry': forms.Select(attrs={'class': 'form-control', 'placeholder': 'ขอนแก่น'}),
            'code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '1234567'}),
            'password': forms.TextInput(attrs={'class': 'form-control', 'disabled': 'true'}),
            'cal_date': forms.DateInput(format=('%d-%m-%Y'),
                                        attrs={'class': 'datepicker input-medium form-control', 'placeholder': 'เลือกวันที่',
                                               'type': 'text',
                                               'onfocus': 'this.showPicker()', 'required': 'true',
                                               'data-provide': "datepicker", 'data-date-language': "th-th",
                                               'autocomplete': "off"}),

        }


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'username')
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'hospital@mail.com'}),
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
        }


class UserCreationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'is_superuser',)
        widgets = {
            'email': forms.EmailInput(
                attrs={'class': 'form-control', 'placeholder': 'hospital@mail.com'}),
            'username': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Username', 'autocomplete': "off"}),
            'password': forms.PasswordInput(
                attrs={'class': 'form-control', 'placeholder': 'Password', 'id': 'password', 'name': 'password',
                       'minlength': '8'}),
            'is_superuser': forms.Select(choices=(
                ('0', 'User'),
                ('1', 'Admin'),
            ), attrs={'class': 'form-control', 'placeholder': 'Permission'}),
        }


class CertificateForm(forms.ModelForm):
    class Meta:
        model = CertificateFile
        fields = ('cert', 'hospital')
        widgets = {
            'cert': forms.FileInput(attrs={'class': 'form-control form-control-lg', 'id': 'upload_input','required': 'true'}),
            # 'hospital': forms.Select(attrs={'class': 'form-control form-control-lg', 'list': 'datalistOptions',
            #                                 'placeholder': "ชื่อโรงพยาบาล", 'type': 'text', 'id': 'datalist_input'})  ,
            'hospital': forms.Select(attrs={
                'class': "js-example-basic-single form-control form-control-lg",
                'name': "state", 'id': 'mySelect2'}),
        }
