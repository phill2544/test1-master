from django import forms
from .models import User_Detail, CertificateFile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class User_DetailForm(forms.ModelForm):
    class Meta:
        model = User_Detail
        fields = ('address', 'province', 'ministry', 'code', 'cal_date')
        widgets = {
            'address': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'ที่อยู่', 'rows': '3'}),
            'province': forms.Select(choices=(
                ('ขอนแก่น', 'ขอนแก่น'),
                ('มหาสารคาม', 'มหาสารคาม'),
                ('ร้อยเอ็ด', 'ร้อยเอ็ด'),
                ('กาฬสินธุ์', 'กาฬสินธุ์'),
            ), attrs={'class': 'form-control', 'placeholder': 'ขอนแก่น'}),
            'ministry': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'กระทรวงสาธารณสุข'}),
            'code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '1234567'}),
            'cal_date': forms.DateInput(format=('%Y-%m-%d'),
                                        attrs={'class': 'form-control', 'placeholder': 'Select Date', 'type': 'date',
                                               'onfocus': 'this.showPicker()', }),

        }
    # user = models.OneToOneField(User, on_delete=models.CASCADE)
    # address = models.TextField(null=True,)
    # province = models.CharField(max_length=60, null=True, default='test')
    # ministry = models.CharField(max_length=60, null=True, default='test')
    # code = models.CharField(max_length=7, null=True, default='test')


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
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'password': forms.PasswordInput(
                attrs={'class': 'form-control', 'placeholder': 'Password', 'id': 'password', 'name': 'password',
                       'minlength': '8'}),
            'is_superuser': forms.Select(choices=(
                ('0', 'User'),
                ('1', 'Admin'),
            ), attrs={'class': 'form-control', 'placeholder': 'Permission'}),
        }
