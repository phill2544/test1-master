import datetime
from datetime import date
import sweetify
from dateutil.relativedelta import relativedelta
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render
from django.http.response import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.urls import reverse
from .models import User_Detail, CertificateFile
from django.contrib.auth.models import User
from .forms import User_DetailForm, UserProfileForm
from django.conf import settings
from . import updater
import os

from django.utils import timezone
from django.core.mail import send_mail


def month(month):
    if month == 1:
        return "มกราคม"
    elif month == 2:
        return "กุมภาพันธ์ "
    elif month == 3:
        return "มีนาคม"
    elif month == 4:
        return "เมษายน"
    elif month == 5:
        return "พฤษภาคม"
    elif month == 6:
        return "มิถุนายน"
    elif month == 7:
        return "กรกฎาคม"
    elif month == 8:
        return "สิงหาคม"
    elif month == 9:
        return "กันยายน"
    elif month == 10:
        return "ตุลาคม"
    elif month == 11:
        return "พฤศจิกายน"
    else:
        return "ธันวาคม"


def delete_file():
    print("delete file")
    certificates = CertificateFile.objects.filter(
        create_date__lte=date.today() + relativedelta(years=-3))  # __lte = less than or equal
    for certificate in certificates:
        os.remove(certificate.cert.path)
        certificate.delete()
    pass


def send_email():
    print('send_Email', settings.EMAIL_HOST_USER)
    users = User_Detail.objects.filter(send_email=False)
    # for user in users:
    #     # print(type(user.cal_date.month))
    #     user.cal_date = date.today()
    #     user.save()
    #     print(user.email)
    if not users:  # No users send email = False
        users = User_Detail.objects.all()
        for user in users:
            user.send_email = False
            user.save()
    for user in users:
        if (user.cal_date + relativedelta(months=-2)) < date.today():
            user.cal_date = (user.cal_date + relativedelta(years=1))
            user.send_email = True
            user.save()
            send_mail(
                "แจ้งนัดล่วงหน้าเพื่อทำการตรวจสอบเครื่องมือแพทย์",
                f'{user.username}ขอเข้าทำการนัดล่วงหน้าเพื่อเข้าไปตรวจสอบเครื่องมือแพทย์ในภายในเดือน{month(user.cal_date.month)}',
                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently=False,
            )

    pass


# Create your views here.
def home(request):
    return HttpResponse('Hello')


@login_required
def certificate(request):
    print(request.user.is_superuser)
    cert = None
    email_authen = None
    email_valid = None
    user = User.objects.get(id=request.user.id)
    if request.method == 'POST':
        try:
            email_authen = request.POST['email']
            email_valid = request.POST['email_valid']
            if email_authen == email_valid:
                user.email = email_authen
                user.save()
            else:
                return render(request, 'general_app/Certificate.html',
                              context={'email_authen': email_authen, 'email_valid': email_valid})
        except:
            cert = request.POST['cert_file']
            hospital_id = User.objects.get(
                username=request.POST['username']).id  # get is a object and filter is multi objects
            certificate_file = CertificateFile.objects.create(cert=cert, hospital_id=hospital_id)
            context = {'certificate_file': request.POST['cert_file']}
            return render(request, 'general_app/Certificate.html', context)
    if request.user.is_authenticated:
        try:
            users = User.objects.all()
            cert = CertificateFile.objects.filter(hospital_id=request.user.id)
        except:
            pass
    context = {'cert': cert, 'email_authen': email_authen, 'email_valid': email_valid, 'users': users}
    return render(request, 'general_app/Certificate.html', context)


@login_required
def profile(request):
    if request.method == "POST":
        form_auth = UserProfileForm(request.POST, instance=request.user)  # instance is update that user request
        form_user = User_DetailForm(request.POST)
        # print(form_auth)
        if form_auth.is_valid() and form_user.is_valid():
            form_auth.save()
            try:
                if User_Detail.objects.get(user_id=request.user.id).user_id:
                    # update
                    a = User_Detail.objects.filter(pk=request.user.user_detail.id).update(
                        province=form_user.cleaned_data['province'],
                        address=form_user.cleaned_data['address'],
                        ministry=form_user.cleaned_data['ministry'],
                        code=form_user.cleaned_data['code'])
            except:
                profile = form_user.save(commit=False)
                profile.user = request.user
                profile.save()
        return HttpResponseRedirect(reverse(('profile')))
    else:
        form_auth = UserProfileForm(instance=request.user)
        try:
            form_user = User_DetailForm(instance=User_Detail.objects.get(pk=request.user.user_detail.id))  # instance
        except:
            form_user = User_DetailForm()
    context = {
        'form_user': form_user,
        'form_auth': form_auth
    }

    return render(request, 'general_app/profile.html', context)


@login_required
def configuration(request):
    return render(request, 'general_app/configuration.html')


@login_required
def manage_user(request):
    users = User.objects.all()
    print(User_Detail.objects.get(user_id=request.user.id))
    print(request.user)
    if request.method == 'POST':
        form_user = User_DetailForm(request.POST, instance=User_Detail.objects.get(user_id=request.user.id))
        if form_user.is_valid():
            form_user.save()
            # form = form_user.save(commit=False)
            # form.user = request.user
            # form.save()
    context = {'users': users}
    return render(request, 'general_app/manage_users.html', context)

@login_required
def edit_user(request, pk):
    users = User.objects.all()
    name = User_Detail.objects.get(user_id=pk)
    if request.method == 'POST':
        form_user = User_DetailForm(request.POST, instance=User_Detail.objects.get(user_id=request.user.id))
        if form_user.is_valid():
            form_user.save()
    # form = {
    #     'province' : request.POST['province'],
    #     'address' : request.POST['address'],
    #     'code' : request.POST['code'],
    #     'cal_date' : request.POST['cal_daet'],
    #     'ministry' : request.POST['ministry'],
    #
    # }
    # province = request.POST['province']
    # address = request.POST['address']
    # code = request.POST['code']
    # cal_date = request.POST['cal_date']
    # ministry = request.POST['ministry']
    try:
        form_user = User_DetailForm(instance=User_Detail.objects.get(user_id=pk))
    except:
        return render(request, 'general_app/manage_users.html',
                      context={'detail_modal': True, 'users': users, 'form_user': None, 'name': name})
    return render(request, 'general_app/manage_users.html',
                  context={'detail_modal': True, 'users': users, 'form_user': form_user, 'name': name})
