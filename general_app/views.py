import datetime
import json
from datetime import date
from xhtml2pdf import pisa
from io import BytesIO
from PyPDF3.pdf import BytesIO
from dateutil.relativedelta import relativedelta
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render
from django.http.response import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import User_Detail, CertificateFile, Configuration, Province, Ministry
from django.contrib.auth.models import User
from .forms import User_DetailForm, UserProfileForm, UserCreationForm, CertificateForm
from django.conf import settings
import os
from django.core.mail import send_mail
from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Table
from reportlab.platypus import SimpleDocTemplate

from django.views.generic import View
from django.template.loader import get_template

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


def date_th(result):
    cert_date = []
    for result_date in result:
        cert_date.append('{} {} {}'.format(result_date.create_date.day, month(result_date.create_date.month),
                                           result_date.create_date.year + 543))
    return cert_date;


def delete_file():
    if Configuration.objects.get(pk=1).delete_date_status:
        try:
            year = int(-Configuration.objects.get(pk=1).delete_date)
        except:
            year = -1
        certificates = CertificateFile.objects.filter(
            create_date__lte=date.today() + relativedelta(years=year))  # __lte = less than or equal
        for certificate in certificates:
            os.remove(certificate.cert.path)
            certificate.delete()
    else:
        pass
    pass


def send_email():
    if Configuration.objects.get(pk=1).sender_mail_status:
        try:
            month = int(-Configuration.objects.get(pk=1).send_mail_date)
            sender_email = Configuration.objects.get(pk=1).sender_mail
        except:
            month = -2
            sender_email = 'example@mail.com'

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
            if (user.cal_date + relativedelta(months=month)) < date.today():
                user.cal_date = (user.cal_date + relativedelta(years=1))
                user.send_email = True
                user.save()
                send_mail(
                    "แจ้งนัดล่วงหน้าเพื่อทำการตรวจสอบเครื่องมือแพทย์",
                    f'{user.username}ขอเข้าทำการนัดล่วงหน้าเพื่อเข้าไปตรวจสอบเครื่องมือแพทย์ในภายในเดือน{month(user.cal_date.month)}',
                    sender_email,
                    [user.email],
                    fail_silently=False,
                )
    else:
        pass
    pass




# def generate_pdf(requset):
#     data = {'user': User.objects.all()}
#     template = get_template('general_app/uploaded_pdf.html')
#     print(data['user'])
#     print()
#     data_p = template.render(data)
#     response = BytesIO()
#     # pdf = pisa.pisaDocument(BytesIO(data_p.encode("UTF-8")), response)
#     pdf = pisa.pisaDocument(BytesIO(data_p.encode("UTF-8")), response)
#     # pdf = pisa.pisaDocument(data_p, response)
#     if not pdf.err:
#         return HttpResponse(response.getvalue(), content_type='application/pdf')
#     return None

# def generate_pdf(request):
#     pass
#     # pdf = pdf('genetal_app/uploaded.html')



def generate_pdf(request):
    buf = io.BytesIO()
    #Create a canvas
    c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
    #create a text object
    textob = c.beginText()
    textob.setTextOrigin(inch,inch)
    # textob.setFont("")

    #Add some line of text
    lines = [
        "ดี ชื่อไร",
        "This is line 2",
        "This is line 3",

    ]

    #loop
    for line in lines:
        textob.textLine(line)


    c.drawText(textob)
    c.showPage()
    c.save()
    buf.seek(0)
    return  FileResponse(buf, as_attachment=True, filename='test.pdf')


@login_required
def home(request):
    try:
        certform = CertificateForm(request.POST, request.FILES)
    except:
        certform = CertificateForm()
    email_authen = None
    email_valid = None
    cert_date = []
    user = User.objects.get(id=request.user.id)
    if request.method == 'POST':
        if 'email' in request.POST:
            email_authen = request.POST['email']
            email_valid = request.POST['email_valid']
            if email_authen == email_valid:
                user.email = email_authen
                user.save()
                messages.success(request, 'email success')
            else:
                messages.success(request, 'emails are not match')
                return render(request, 'general_app/home.html',
                              context={'email_authen': email_authen, 'email_valid': email_valid})
        elif request.FILES:
            if certform.is_valid():
                certform.save()
                # instance = certform.save(commit=False)
                # instance.hospital_id = User.objects.get(username=request.POST['username']).id  # get is a object and filter is multi objects
                # instance.save()
                # hospital_id = User.objects.get(
                #     username=request.POST['hospital']).id  # get is a object and filter is multi objects
                # CertificateFile.objects.create(cert=certform.cleaned_data['cert'].name, hospital_id=hospital_id)
            # cert_file = request.FILES['cert_file']
            # hospital_id = User.objects.get(
            #     username=request.POST['username']).id  # get is a object and filter is multi objects
            # CertificateFile.objects.create(cert=cert_file.name, hospital_id=hospital_id)
            # fs = FileSystemStorage()
            # fs.save(cert_file.name, cert_file)
            # messages.success(request, 'uploaded file')
            return HttpResponseRedirect(reverse('home'))
            # return render(request, 'general_app/home.html', context)
        elif 'delete_file' in request.POST:
            delete_files = str(request.POST)
            delete_files = delete_files[delete_files.index('delete_file') + 16:delete_files.index(']}>') - 5].split(',')
            for delete_file in delete_files:
                certificate_file = CertificateFile.objects.get(pk=delete_file)
                os.remove(certificate_file.cert.path)
                certificate_file.delete()
            return HttpResponseRedirect(reverse('home'))
        # elif 'btn_sort' in request.POST:
        #     pass
        # return render(request, 'general_app/home.html',
        #               {'certs': zip(result, cert_date), 'certform': certform})

    elif 'searched' in request.GET or 'date_filter' in request.GET:  # and request.GET['searched'] is not ''
        result = []
        searched = request.GET['searched'] if request.GET['searched'] else ''
        date_filter = request.GET['date_filter'] if request.GET['date_filter'] else ''
        date_filter = date_filter.split('-') if date_filter else ''
        # result = CertificateFile.objects.filter(create_date__month=date_filter[1], create_date__year=date_filter[0])
        try:
            username_id = User.objects.get(username__contains=searched).id
            search_cert = CertificateFile.objects.filter(hospital_id=username_id)
        except:
            username_id = User.objects.filter(username__contains=searched)
            search_cert = CertificateFile.objects.filter(hospital_id__in=username_id)
        if date_filter != '':
            for cert in search_cert:
                if cert.create_date.month == int(date_filter[1]) and cert.create_date.year == int(date_filter[0]):
                    result.append(cert)
            cert_date = date_th(result)
            return render(request, 'general_app/home.html',
                          {'searched': searched, 'certs': zip(result, cert_date), 'certform': certform})
        cert_date = date_th(search_cert)
        return render(request, 'general_app/home.html',
                      {'searched': searched, 'certs': zip(search_cert, cert_date), 'certform': certform})
    elif 'date_filter' in request.GET:
        date_filter = request.GET['date_filter'].split('-')
        result = CertificateFile.objects.filter(create_date__month=date_filter[1], create_date__year=date_filter[0])
        cert_date = date_th(result)
        return render(request, 'general_app/home.html',
                      {'certs': zip(result, cert_date), 'certform': certform})
    if request.user.is_authenticated:
        try:
            users = User.objects.all()
            if request.user.is_superuser:
                certs = CertificateFile.objects.filter()
            else:
                certs = CertificateFile.objects.filter(hospital_id=request.user.id)
            # date_th(cert)
        except:
            certs = CertificateFile.objects.filter()
    cert_date = date_th(certs)

    context = {'certs': zip(certs, cert_date), 'email_authen': email_authen, 'email_valid': email_valid,
               'users': users, 'certform': certform}
    return render(request, 'general_app/home.html', context)


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
    form_configuration = Configuration.objects.get(pk=1)
    province = Province.objects.all()
    ministry = Ministry.objects.all()
    state = None
    if request.method == "POST":
        if 'add_province' in request.POST:
            Province.objects.create(province=request.POST['add_province'])
            state = 'เพิ่มจังหวัด {} เสร็จสิ้น'.format(request.POST['add_province'])
        elif 'add_ministry' in request.POST:
            Ministry.objects.create(ministry=request.POST['add_ministry'])
            state = 'เพิ่มกระทรวง {} เสร็จสิ้น'.format(request.POST['add_ministry'])
        elif 'select_province' in request.POST:
            Province.objects.filter(province=request.POST['select_province']).delete()
            state = 'ลบจังหวัด {} เสร็จสิ้น'.format(request.POST['select_province'])
        elif 'select_ministry' in request.POST:
            Ministry.objects.filter(ministry=request.POST['select_ministry']).delete()
            state = 'ลบกระทรวง {} เสร็จสิ้น'.format(request.POST['select_ministry'])
        elif 'is_send' in request.POST:
            form_configuration.sender_mail_status = not form_configuration.sender_mail_status
            form_configuration.save()
        elif 'is_delete' in request.POST:
            form_configuration.delete_date_status = not form_configuration.delete_date_status
            form_configuration.save()
        else:
            config = Configuration.objects.get(pk=1)
            config.send_mail_date = request.POST['send_mail_date']
            config.delete_date = request.POST['delete_date']
            config.sender_mail = request.POST['sender_mail']
            config.save()
            state = 'เปลี่ยนการตั้งค่าเสร็จสิ้น'
    context = {'form_configuration': form_configuration, 'province': province, 'ministry': ministry, 'state': state}
    return render(request, 'general_app/configuration.html', context)


@login_required
def manage_user(request):
    try:
        a = Configuration.objects.get(id=1).delete_date
    except:
        a = -2
    users = User.objects.all()
    if request.method == 'POST':
        form_user_detail = User_DetailForm(request.POST)
        form_user_creation = UserCreationForm(request.POST)
        if form_user_creation.data['password'] == form_user_creation.data['confirm_password']:
            if form_user_detail.is_valid() and form_user_creation.is_valid():
                form_user_creation = User.objects.create_user(request.POST['username'], request.POST['email'],
                                                              request.POST['password'],
                                                              is_superuser=request.POST['is_superuser'])
                form_user_detail = User_Detail.objects.create(province_id=request.POST['province'],
                                                              address=request.POST['address'],
                                                              ministry_id=request.POST['ministry'],
                                                              cal_date=request.POST['cal_date'],
                                                              user_id=form_user_creation.id, code=request.POST['code'])
                form_user_creation.save()
                form_user_detail.save()
                form_user_detail = User_DetailForm()
                form_user_creation = UserCreationForm()
                context = {'add_user': True, 'users': users, 'form_user_creation': form_user_creation,
                           'form_user_detail': form_user_detail, 'username': request.POST['username']}
                return render(request, 'general_app/manage_users.html', context)
            else:
                form_user_creation = form_user_creation
                form_user_detail = form_user_detail
                form_user_creation.username = ''
                context = {'exist_user': True, 'form_user_creation': form_user_creation,
                           'form_user_detail': form_user_detail, 'users': users}
                return render(request, 'general_app/manage_users.html', context)
        else:  # password not match
            form_user_creation = form_user_creation
            form_user_detail = form_user_detail
            context = {'Is_passowrd': True, 'form_user_creation': form_user_creation,
                       'form_user_detail': form_user_detail, 'users': users}
            return render(request, 'general_app/manage_users.html', context)
    form_user_detail = User_DetailForm()
    form_user_creation = UserCreationForm()
    context = {'users': users, 'form_user_detail': form_user_detail, 'form_user_creation': form_user_creation}
    return render(request, 'general_app/manage_users.html', context)


@login_required
def edit_user(request, pk):
    users = User.objects.all()
    try:
        name = User_Detail.objects.get(user_id=pk)
    except:
        pass
    if request.method == 'POST':
        if 'delete_user' in request.POST:
            try:
                User.objects.get(id=pk).delete()
                return HttpResponseRedirect(reverse('manage_user'))
            except User.DoesNotExist:
                messages.error(request, 'User does not exist')
                return HttpResponseRedirect(reverse('manage_user'))
        else:
            form_user_detail = User_DetailForm(request.POST, instance=User_Detail.objects.get(user_id=name.user_id))
            form_user = UserProfileForm(request.POST, instance=User.objects.get(id=name.user_id))
            if form_user_detail.is_valid() and form_user.is_valid():
                form_user.save()
                form_user_detail.save()
                return HttpResponseRedirect(reverse('manage_user'))
                # return HttpResponseRedirect(reverse('manage_user'))
    try:
        form_user_detail = User_DetailForm(instance=User_Detail.objects.get(user_id=pk))
        form_user = UserProfileForm(instance=User.objects.get(id=pk))
    except:
        return render(request, 'general_app/manage_users.html',
                      context={'detail_modal': True, 'users': users, 'form_user': None, 'name': name,
                               'form_user_email': None})
    context = {'detail_modal': True, 'users': users, 'form_user': form_user_detail, 'name': name,
               'form_user_email': form_user}
    return render(request, 'general_app/manage_users.html', context)
