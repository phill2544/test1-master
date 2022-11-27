from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.http.response import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User

# Create your views here.
from django.urls import reverse
import sweetify

def login_user(request):
    if not request.user.is_authenticated: # not login yet
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)  # check user and password
            print(user)
            if user is not None:
                login(request, user)
                sweetify.sweetalert(request, 'Westworld is awesome',text='Really... if you have the chance - watch it!', persistent='I agree!')
                return redirect('certificate',)
            else:
                messages.success(request,('Got something wrong'))
                redirect('login')

    else:
        return HttpResponseRedirect(reverse('certificate'))
    return render(request, 'registration/login.html',context={'user':User.objects.all()})
