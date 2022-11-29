from django import forms
from .models import User_Detail, CertificateFile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class User_DetailForm(forms.ModelForm):
    class Meta:
        model = User_Detail
        fields = ('address', 'province', 'ministry', 'code')
        widgets = {
            'address': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'ที่อยู่', 'rows': '3'}),
            'province': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ขอนแก่น'}),
            'ministry': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'กระทรวงสาธารณสุข'}),
            'code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '1234567'}),
        }
    # user = models.OneToOneField(User, on_delete=models.CASCADE)
    # address = models.TextField(null=True,)
    # province = models.CharField(max_length=60, null=True, default='test')
    # ministry = models.CharField(max_length=60, null=True, default='test')
    # code = models.CharField(max_length=7, null=True, default='test')


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email',)
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'hospital@mail.com'})
        }


