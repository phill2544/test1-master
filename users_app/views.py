import requests
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
from django.contrib.auth.views import PasswordChangeView
from general_app.models import User_Detail


# def change_password(request,PasswordChangeView):
#     form_class = PasswordChangingForm

def login_user(request):
    if not request.user.is_authenticated:  # not login yet
        if request.method == 'POST':
            username = request.POST['username']
            user_id = User.objects.get(username = request.POST['username']).id
            password = request.POST['password']
            user = authenticate(username=username, password=password)  # check user and password
            if user is not None:
                if user.is_active:
                    try:#deleting session
                        del request.session['user']
                    except:
                        pass
                    messages.success(request, 'login success')
                    login(request, user)
                    return redirect('home')
                    # return redirect('certificate')
                # else:
                #     return render(request, 'registration/login.html', context={'login': 'login'})
            else:
                messages.success(request, 'Got something wrong')
                request.session['user'] = {'username': request.POST['username'],
                                           'user_id':user_id}
                return redirect('login')

    else:  # logged in
        return HttpResponseRedirect(reverse('home'))
    users = []
    for user in User.objects.all():
        users.append(user.username)
    context = {
        'user': users
    }
    return render(request, 'registration/login.html', context)


def changepassword_done(request):
    return HttpResponseRedirect(reverse('home'))


def change_password(request):
    if request.method == "POST":
        user_id = User.objects.get(username=request.user).id
        old_password = User_Detail.objects.get(user_id=user_id).password
        if request.POST['old_password'] == old_password:
            set_password = User.objects.get(id=user_id)
            set_password.set_password(str(request.POST['new_password2']))
            set_password.save()
            User_Detail.objects.filter(user_id=user_id).update(password=str(request.POST['new_password2']))
    return render(request, 'registration/change_password.html')
