from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django import forms

# class PasswordChangingForm(PasswordChangeForm):
#     class Meta:
#         model = User
#         fields = ('old_password','new_password1','new_password2')
#         widgets = {
#             'old_password': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'hospital@mail.com'}),
#             'new_password1': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
#             'new_password2': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
#         }


