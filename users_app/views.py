from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.http.response import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.template.loader import render_to_string

# Create your views here.
from django.urls import reverse

from general_app.models import CertificateFile


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
                    cert = CertificateFile.objects.filter(hospital_id=request.user.id)
                    return redirect('certificate')
                else:
                    return render(request, 'registration/login.html', context={'login': 'login', 'cert': cert})
            else:
                messages.success(request, ('Got something wrong'))
                redirect('login')

    else:
        return HttpResponseRedirect(reverse('certificate'))
    return render(request, 'registration/login.html', context={'user': User.objects.all()})
