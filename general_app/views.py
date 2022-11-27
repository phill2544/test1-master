import datetime
from datetime import date

from dateutil.relativedelta import relativedelta
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http.response import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Employee, CertificateFile
from django.contrib.auth.models import User
from .forms import EmployeeForm, UserProfileForm
from django.conf import settings
from . import updater

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
    # print(date.today().replace(month=1,day=1))
    certificates = CertificateFile.objects.filter(
        create_date__lte=date.today().replace(month=1, day=1) + relativedelta(years=-3))  # __lte = less than or equal
    for certificate in certificates:
        certificate.delete()
    pass


def send_email():
    print('send_Email',settings.EMAIL_HOST_USER)
    users = Employee.objects.filter(send_email=False)
    # for user in users:
    #     # print(type(user.cal_date.month))
    #     user.cal_date = date.today()
    #     user.save()
    #     print(user.email)
    if not users:  # No users send email = False
        users = Employee.objects.all()
        for user in users:
            user.send_email = False
            user.save()

    for user in users:
        if (user.cal_date + relativedelta(months=-2)) < date.today():
            username = user.username
            months = month(user.cal_date.month)
            user.cal_date = (user.cal_date + relativedelta(years=1))
            user.send_email = True
            user.save()
            send_mail(
                "แจ้งนัดล่วงหน้าเพื่อทำการตรวจสอบเครื่องมือแพทย์",
                f'{username}ขอเข้าทำการนัดล่วงหน้าเพื่อเข้าไปตรวจสอบเครื่องมือแพทย์ในภายในเดือน{months}',
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
    # send_mail(
    #     'Test again',
    #     'Here is the message.',
    #     'sayomphu.su@rmuti.ac.th',
    #     ['phill2544@gmail.com'],
    #     fail_silently=False,
    # )
    # print('mail')
    cert = None
    email_authen = None
    user = User.objects.get(id=request.user.id)
    if request.method == 'POST':
        email_authen = request.POST['email_cert']
        email = request.POST['email_cert']
        user.email = email
        user.save()
    if request.user.is_authenticated:
        try:
            cert = CertificateFile.objects.filter(hospital_id=request.user.id)
        except:
            pass
    context = {'cert': cert, 'email_authen': email_authen}
    return render(request, 'general_app/Certificate.html', context)


@login_required
def profile(request):
    if request.method == "POST":
        form_auth = UserProfileForm(request.POST, instance=request.user)  # instance is update that user request
        form_employee = EmployeeForm(request.POST)
        # print(form_auth)
        if form_auth.is_valid() and form_employee.is_valid():
            form_auth.save()
            try:
                if Employee.objects.get(user_id=request.user.id).user_id:
                    # update
                    a = Employee.objects.filter(pk=request.user.employee.id).update(
                        province=form_employee.cleaned_data['province'],
                        address=form_employee.cleaned_data['address'],
                        ministry=form_employee.cleaned_data['ministry'],
                        code=form_employee.cleaned_data['code'])
            except:
                profile = form_employee.save(commit=False)
                profile.user = request.user
                profile.save()
        return HttpResponseRedirect(reverse(('profile')))
    else:
        form_auth = UserProfileForm(instance=request.user)
        try:
            form_employee = EmployeeForm(instance=Employee.objects.get(pk=request.user.employee.id))  # instance
        except:
            form_employee = EmployeeForm()
    context = {
        'form_employee': form_employee,
        'form_auth': form_auth
    }

    return render(request, 'general_app/profile.html', context)
