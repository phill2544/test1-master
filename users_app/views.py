
from django.contrib.auth import authenticate, login, logout
from django.http.response import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User

# Create your views here.
from django.urls import reverse
from general_app.models import CertificateFile
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect

def change_password(request):
    if request.method == 'POST':
        user = User.objects.get(username__exact=request.user)
        user.set_password(request.POST['new_password2'])
    return render(request,'registration/password_change_form.html')

def login_user(request):
    if not request.user.is_authenticated:  # not login yet
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)  # check user and password
            if user is not None:
                if user.is_active:
                    login(request, user)
                    # return redirect('certificate')
                    return redirect('certificate')
                    # return redirect('certificate')
                # else:
                #     return render(request, 'registration/login.html', context={'login': 'login'})
            else:
                messages.success(request, ('Got something wrong'))
                redirect('login')

    else:
        return HttpResponseRedirect(reverse('certificate'))
    return render(request, 'registration/login.html', context={'user': User.objects.all()})
