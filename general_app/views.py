import datetime
import json
from datetime import date

from django.core import serializers
from django.template import Template, Context
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
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
from .models import User_Detail, CertificateFile, Configuration, Province, Ministry, Verify_Certificatefile
from django.contrib.auth.models import User
from .forms import User_DetailForm, UserProfileForm, UserCreationForm, CertificateForm, Verify_CertificateForm
from django.conf import settings
import os
from django.core.mail import send_mail
from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Table, TableStyle, Spacer, Paragraph
from reportlab.platypus import SimpleDocTemplate

from django.views.generic import View
from django.template.loader import get_template, render_to_string
from fpdf import FPDF
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from django.contrib.staticfiles import finders


def month(month, short=None):
    if month == 1:
        if short:
            return "ม.ค."
        else:
            return "มกราคม"
    elif month == 2:
        if short:
            return "ก.พ."
        else:
            return "กุมภาพันธ์ "
    elif month == 3:
        if short:
            return "มี.ค."
        else:
            return "มีนาคม"
    elif month == 4:
        if short:
            return "เม.ย."
        else:
            return "เมษายน"
    elif month == 5:
        if short:
            return "พ.ค."
        else:
            return "พฤษภาคม"
    elif month == 6:
        if short:
            return "มิ.ย."
        else:
            return "มิถุนายน"
    elif month == 7:
        if short:
            return "ก.ค."
        else:
            return "กรกฎาคม"
    elif month == 8:
        if short:
            return "ส.ค."
        else:
            return "สิงหาคม"
    elif month == 9:
        if short:
            return "ก.ย."
        else:
            return "กันยายน"
    elif month == 10:
        if short:
            return "ต.ค."
        else:
            return "ตุลาคม"
    elif month == 11:
        if short:
            return "พ.ย."
        else:
            return "พฤศจิกายน"
    else:
        if short:
            return "ธ.ค."
        else:
            return "ธันวาคม"


def date_th(result):
    cert_date = []
    try:
        for result_date in result:
            cert_date.append('{} {} {}'.format(result_date.create_date.day, month(result_date.create_date.month),
                                               result_date.create_date.year + 543))
    except:
        cert_date.append('{} {} {}'.format(result.create_date.day, month(result.create_date.month),
                                           result.create_date.year + 543))
    return cert_date


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


# def create_pdf(request):
#     # Create the PDF document
#     pdfmetrics.registerFont(TTFont('ThaiFont', 'general_app/THSarabunNew.ttf'))
#
#     # Create the PDF document
#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = 'attachment; filename="report.pdf"'
#     doc = SimpleDocTemplate(response, pagesize=letter)
#     styles = getSampleStyleSheet()
#
#     # Set the font in the CSS style
#     styles.add(ParagraphStyle(name='ThaiStyle', fontName='ThaiFont', fontSize=12))
#
#     # Parse the HTML
#     html = '<html><body><H1>มาเพื่อ</H1></body></html>'
#     elements = []
#     elements.append(Paragraph(html, styles['ThaiStyle']))
#
#     # Build the PDF
#     doc.build(elements)
#     return response


# def create_pdf(request):
#
#     elems = []
#     data = []
#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = 'attachment; filename="table.pdf"'
#
#     buffer = BytesIO()
#     doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=5,
#                             leftMargin=5,
#                             topMargin=5,
#                             bottomMargin=5)
#     #
#     # pdf = SimpleDocTemplate(
#     #     'mypdf.pdf',
#     #     pagesize=letter,
#     # )
#     pdfmetrics.registerFont(TTFont('THSarabun', 'general_app/THSarabunNew.ttf'))
#     pdfmetrics.registerFont(TTFont('THSarabunB', 'general_app/THSarabunNew Bold.ttf'))
#     #
#     # header = [
#     #     Spacer(1, 5 * cm),
#     #     Paragraph('ศูนย์สนับสนุนบริการสุขภาพที่',ParagraphStyle('test',fontName='general_app/THSarabunNew.ttf')),
#     #     Spacer(1, 5 * cm),
#     # ]
#     data += [
#         # header,
#         # ['', 'ศูนย์สนับสนุนบริการสุขภาพที่ 7', ''],
#         ['อัปโหลดแล้ว', '{}/{}'.format(User_Detail.objects.filter(is_upload=True).count(), User.objects.all().count())],
#         ['ดาวโหลดแล้ว',
#          '{}/{}'.format(CertificateFile.objects.filter(count_download__gt=0).count(), User.objects.all().count())],
#         ['', '', ''],
#         ['โรงพยาบาล', 'วันที่อัปโหลด', 'จำนวนการดาวโหลด'],
#     ]
#
#     for user in User.objects.all():
#         if User_Detail.objects.get(user_id=user.id).is_upload:
#             # if not CertificateFile.objects.filter(hospital_id=user.id).order_by('-create_date'):
#             #     upload = ''
#             #     count_download = 0
#             # else:
#             upload = CertificateFile.objects.filter(hospital_id=user.id).order_by('-create_date')[0]
#             count_download = upload.count_download
#             upload = upload.create_date + relativedelta(years=543)
#         else:
#             upload = ''
#             count_download = ''
#         try:
#             date_upload = '{} {} {}'.format(upload.day, month(int(upload.month), True), upload.year)
#         except:
#             date_upload = ''
#         data += [
#             ['{}'.format(user.username),
#              date_upload,
#              '{}'.format(count_download)]
#         ]
#
#     # obj = {User.objects.all()}
#     # pdf.drawString(2 * cm, 27 * cm, str(obj))
#     table = Table(data, colWidths=6 * cm, rowHeights=1 * cm, vAlign='TOP', )
#     table.setStyle(TableStyle([
#         ('FONT', (0, 0), (1, 1), 'THSarabun'),
#         ('FONTSIZE', (0, 0), (1, 1), 20),
#         ('FONT', (0, 3), (2, 3), 'THSarabunB'),
#         ('FONTSIZE', (0, 3), (2, 3), 20),  # header
#         ('FONT', (0, 4), (-1, -1), 'THSarabun'),
#         ('FONTSIZE', (0, 4), (-1, -1), 20),
#         # ('FONTSIZE', (0, 0), (-1, 0), 50),
#         # ('BOX', (0, 3), (-1, -1), 1, (0, 0, 0)),
#         ('BOX', (0, 0), (1, 1), 1, (0, 0, 0)),  # box in content
#         ('INNERGRID', (0, 0), (1, 1), 0.25, colors.black),
#         ('LINEBELOW', (0, 3), (-1, -1), 0.5, colors.black),
#         # ('TEXTCOLOR', (0, 0), (-1, 0), colors.red),
#         ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
#         ('VALIGN', (0, 0), (-1, -1), 'TOP'),
#         # ('LINEBEFORE', (0, 0), (1,1), 2, colors.black),
#         # ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
#     ]))
#     elems = [table]
#     # Save the PDF
#     doc.build(elems)
#     # pdf.save()
#
#     pdf = buffer.getvalue()
#     buffer.close()
#     response.write(pdf)
#
#     return response


def create_pdf(datas):
    elems = []
    data = []
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="table.pdf"'

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=5,
                            leftMargin=5,
                            topMargin=10,
                            bottomMargin=5)
    #
    # pdf = SimpleDocTemplate(
    #     'mypdf.pdf',
    #     pagesize=letter,
    # )
    pdfmetrics.registerFont(TTFont('THSarabun', 'general_app/THSarabunNew.ttf'))
    pdfmetrics.registerFont(TTFont('THSarabunB', 'general_app/THSarabunNew Bold.ttf'))
    #
    # header = [
    #     Spacer(1, 5 * cm),
    #     Paragraph('ศูนย์สนับสนุนบริการสุขภาพที่',ParagraphStyle('test',fontName='general_app/THSarabunNew.ttf')),
    #     Spacer(1, 5 * cm),
    # ]
    data += [
        # header,
        # ['', 'ศูนย์สนับสนุนบริการสุขภาพที่ 7', ''],
        ['อัปโหลดแล้ว', '{}/{}'.format(User_Detail.objects.filter(is_upload=True).count(), User.objects.all().count())],
        ['ดาวน์โหลดแล้ว',
         '{}/{}'.format(CertificateFile.objects.filter(count_download__gt=0).count(), User.objects.all().count())],
        ['', '', ''],
        ['โรงพยาบาล', 'วันที่อัปโหลด', 'จำนวนการดาวน์โหลด'],
    ]

    # for user in User.objects.all():
    #     if User_Detail.objects.get(user_id=user.id).is_upload:
    #         # if not CertificateFile.objects.filter(hospital_id=user.id).order_by('-create_date'):
    #         #     upload = ''
    #         #     count_download = 0
    #         # else:
    #         upload = CertificateFile.objects.filter(hospital_id=user.id).order_by('-create_date')[0]
    #         count_download = upload.count_download
    #         upload = upload.create_date + relativedelta(years=543)
    #     else:
    #         upload = ''
    #         count_download = ''
    #     try:
    #         date_upload = '{} {} {}'.format(upload.day, month(int(upload.month), True), upload.year)
    #     except:
    #         date_upload = ''
    for count, item in datas.items():
        data += [
            [item['hospital'],
             item['upload_date'],
             item['count_download']]
        ]

    # obj = {User.objects.all()}
    # pdf.drawString(2 * cm, 27 * cm, str(obj))
    table = Table(data, colWidths=6 * cm, rowHeights=1 * cm, vAlign='TOP', )
    table.setStyle(TableStyle([
        ('FONT', (0, 0), (1, 1), 'THSarabun'),
        ('FONTSIZE', (0, 0), (1, 1), 20),
        ('FONT', (0, 3), (2, 3), 'THSarabunB'),
        ('FONTSIZE', (0, 3), (2, 3), 20),  # header
        ('FONT', (0, 4), (-1, -1), 'THSarabun'),
        ('FONTSIZE', (0, 4), (-1, -1), 20),
        # ('FONTSIZE', (0, 0), (-1, 0), 50),
        # ('BOX', (0, 3), (-1, -1), 1, (0, 0, 0)),
        ('BOX', (0, 0), (1, 1), 1, (0, 0, 0)),  # box in content
        ('INNERGRID', (0, 0), (1, 1), 0.25, colors.black),
        ('LINEBELOW', (0, 3), (-1, -1), 0.5, colors.black),
        # ('TEXTCOLOR', (0, 0), (-1, 0), colors.red),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        # ('LINEBEFORE', (0, 0), (1,1), 2, colors.black),
        # ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    elems = [table]
    # Save the PDF
    doc.build(elems)
    # pdf.save()

    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response


@login_required
def home(request, hospital_id=None):
    # try:
    #     certform = CertificateForm(request.POST, request.FILES)
    # except:
    #     certform = CertificateForm()
    email_authen = None
    email_valid = None
    searched = None
    cert_date = []
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
    user = User.objects.get(id=request.user.id)
    if request.method == 'POST':
        if 'email' in request.POST:
            position = request.POST['position']
            name = request.POST['name']
            number = request.POST['number']
            email_authen = request.POST['email']
            email_valid = request.POST['email_valid']
            if email_authen == email_valid:
                User_Detail.objects.filter(user_id=request.user.id).update(position=position, number=number)
                name_split = str(name).split()
                user.email = email_authen
                # if name_split.__len__() >= 3 :
                #     for count in name_split:
                #         name_split[0] += name_split[count]
                #         if count == name_split.__len__() - 2:
                #             break
                try:
                    user.first_name = name_split[0]
                    user.last_name = name_split[1]
                except:
                    user.first_name = name_split[0]
                # user_detail[0].position = position
                # user_detail[0].number = number
                # user_detail[0].save()
                user.save()
                messages.success(request, 'email success')
            else:
                messages.success(request, 'emails are not match')
                return render(request, 'general_app/home.html',
                              context={'email_authen': email_authen, 'email_valid': email_valid,
                                       'name': name,
                                       'position': position,
                                       'number': number})
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
        searched = request.GET.getlist('searched') if request.GET.getlist('searched') else ''
        # date_filters = request.GET['date_filter'] if request.GET['date_filter'] else ''
        # date_filter = date_filters.split('-') if date_filters else ''
        # result = CertificateFile.objects.filter(create_date__month=date_filter[1], create_date__year=date_filter[0])
        try:
            username_id = User.objects.get(username__contains=searched).id
            certs = CertificateFile.objects.filter(hospital_id=username_id)
        except:
            username_id = User.objects.filter(username__in=searched)
            certs = CertificateFile.objects.filter(hospital_id__in=username_id)
        # if date_filter != '':
        #     for cert in certs:
        #         if cert.create_date.month == int(date_filter[1]) and cert.create_date.year == int(date_filter[0]):
        #             result.append(cert)
        #     cert_date = date_th(result)
        #     return render(request, 'general_app/home.html',
        #                   {'searched': searched, 'certs': zip(result, cert_date), 'certform': certform,
        #                    'date_filter': date_filters, 'users': users})
        cert_date = date_th(certs)
        return render(request, 'general_app/home.html',
                      {'searched': searched, 'certs': zip(certs, cert_date), 'users': users})  # 'certform': certform,
    elif 'date_filter' in request.GET:
        date_filter = request.GET['date_filter'].split('-')
        result = CertificateFile.objects.filter(create_date__month=date_filter[1], create_date__year=date_filter[0])
        cert_date = date_th(result)
        return render(request, 'general_app/home.html',
                      {'certs': zip(result, cert_date)})  # , 'certform': certform
    elif hospital_id != None:
        if not request.user.is_superuser:
            count_download = CertificateFile.objects.get(pk=hospital_id).count_download + 1
            CertificateFile.objects.filter(pk=hospital_id).update(count_download=count_download)
            return HttpResponseRedirect(reverse('home'))
        else:
            return HttpResponseRedirect(reverse('home'))
    cert_date = date_th(certs)
    context = {'certs': zip(certs, cert_date), 'email_authen': email_authen, 'email_valid': email_valid,
               'users': users, 'searched': searched}  # 'certform': certform,
    return render(request, 'general_app/home.html', context)


@login_required
def profile(request):
    if request.method == "POST":
        form_auth = UserProfileForm(request.POST, instance=request.user)  # instance is update that user request
        form_user = User_DetailForm(request.POST)
        # print(form_auth)
        if form_user.is_valid():
            User.objects.filter(id=request.user.id).update(email=request.POST['email'])
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
        'form_auth': form_auth,
        'user_information': {
            'user': User.objects.get(id=request.user.id),
            'detail': User_Detail.objects.get(user_id=request.user.id)
        }
    }

    return render(request, 'general_app/profile.html', context)


@login_required
def configuration(request):
    try:
        form_configuration = Configuration.objects.get(pk=1)
    except:
        form_configuration = Configuration.objects.create(pk=1)
    state = None
    if request.method == "POST":
        if 'add_province' in request.POST:
            try:
                Province.objects.filter(province=request.POST['add_province']).update(is_show=1)
            except:
                Province.objects.create(province=request.POST['add_province'])
            state = 'เพิ่มจังหวัด {} เสร็จสิ้น'.format(request.POST['add_province'])
        elif 'add_ministry' in request.POST:
            try:
                Ministry.objects.filter(province=request.POST['add_ministry']).update(is_show=1)
            except:
                Ministry.objects.create(province=request.POST['add_ministry'])
            Ministry.objects.create(ministry=request.POST['add_ministry'])
            state = 'เพิ่มกระทรวง {} เสร็จสิ้น'.format(request.POST['add_ministry'])
        elif 'select_province' in request.POST:
            Province.objects.filter(province=request.POST['select_province']).update(is_show=False)
            state = 'ลบจังหวัด {} เสร็จสิ้น'.format(request.POST['select_province'])
        elif 'select_ministry' in request.POST:
            Ministry.objects.filter(ministry=request.POST['select_ministry']).update(is_show=False)
            state = 'ลบกระทรวง {} เสร็จสิ้น'.format(request.POST['select_ministry'])
        elif 'is_send' in request.POST:
            form_configuration.sender_mail_status = not form_configuration.sender_mail_status
            form_configuration.save()
            return HttpResponseRedirect(reverse('configuration'))
        elif 'is_delete' in request.POST:
            form_configuration.delete_date_status = not form_configuration.delete_date_status
            form_configuration.save()
            return HttpResponseRedirect(reverse('configuration'))
        else:
            config = Configuration.objects.get(pk=1)
            config.send_mail_date = request.POST['send_mail_date']
            config.delete_date = request.POST['delete_date']
            config.sender_mail = request.POST['sender_mail']
            config.save()
            state = 'เปลี่ยนการตั้งค่าเสร็จสิ้น'
    province = Province.objects.filter(is_show=True)
    ministry = Ministry.objects.filter(is_show=True)
    context = {'form_configuration': Configuration.objects.get(pk=1), 'province': province, 'ministry': ministry,
               'state': state}
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
        date = request.POST['cal_date']
        # cal_date = request.POST['cal_date']
        cal_date = '{}-{}-{}'.format(int(str(date).split('-')[2]) - 543, str(date).split('-')[1],
                                     str(date).split('-')[0])
        if form_user_creation.data['password'] == form_user_creation.data['confirm_password']:
            if form_user_detail:
                form_user_creation = User.objects.create_user(request.POST['username'], request.POST['email'],
                                                              request.POST['password'],
                                                              is_superuser=request.POST['is_superuser'])
                form_user_detail = User_Detail.objects.create(province_id=request.POST['province'],
                                                              address=request.POST['address'],
                                                              ministry_id=request.POST['ministry'],
                                                              cal_date=str(cal_date),
                                                              user_id=form_user_creation.id,
                                                              code=request.POST['code'],
                                                              password=request.POST['password'])
                form_user_creation.save()
                form_user_detail.save()
                form_user_detail = User_DetailForm()
                form_user_creation = UserCreationForm()
                context = {'add_user': True, 'users': users, 'form_user_creation': form_user_creation,
                           'form_user_detail': form_user_detail, 'username': request.POST['username'],
                           'current_date': '{}-{}-{}'.format(datetime.date.today().day, datetime.date.today().month,
                                                             int(datetime.date.today().year) + 543)}
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
    form_user_detail.fields['province'].queryset = Province.objects.filter(is_show=True)
    form_user_creation = UserCreationForm()
    context = {'users': users, 'form_user_detail': form_user_detail, 'form_user_creation': form_user_creation}
    return render(request, 'general_app/manage_users.html', context)


@login_required
def edit_user(request, pk):
    print("edit_user")
    users = User.objects.all()
    try:
        name = User_Detail.objects.get(user_id=pk)
    except:
        name = User_Detail.objects.create(user_id=pk)
    if request.method == 'POST':
        form_user_detail = User_DetailForm(request.POST, instance=User_Detail.objects.get(user_id=name.user_id))
        user = User.objects.filter(id=pk)
        form_user = UserProfileForm(request.POST, instance=User.objects.get(id=name.user_id))
        cal_date = form_user.data['cal_date'].split('-')
        User_Detail.objects.filter(user_id=pk).update(province_id=form_user_detail.data['province'],
                                                      ministry_id=form_user_detail.data['ministry'],
                                                      code=form_user_detail.data['code'],
                                                      address=form_user_detail.data['address'],
                                                      cal_date='{}-{}-{}'.format(str(int(cal_date[2]) - 543),
                                                                                 cal_date[1], cal_date[0]),
                                                      position=request.POST['position'])
        User.objects.filter(id=pk).update(email=form_user_detail.data['email'], first_name=request.POST['first_name'],
                                          last_name=request.POST['last_name'])
        user.update(email=request.POST['email'])
        return HttpResponseRedirect(reverse('manage_user'))
        # return HttpResponseRedirect(reverse('manage_user'))
    try:
        user_detail_information = User_Detail.objects.get(user_id=pk)
        form_user_detail = User_DetailForm(instance=user_detail_information)
        form_user_detail.initial.update(cal_date=datetime.date(user_detail_information.cal_date.year + 543,
                                                               user_detail_information.cal_date.month,
                                                               user_detail_information.cal_date.day))
        if name.province.is_show:  # show only province
            form_user_detail.fields['province'].queryset = Province.objects.filter(is_show=True)
        form_user = UserProfileForm(instance=user_detail_information)
        user_information = {
            'user': User.objects.get(id=pk),
            'detail': User_Detail.objects.get(user_id=pk)
        }
    except:
        return render(request, 'general_app/manage_users.html',
                      context={'detail_modal': True, 'users': users, 'form_user': None, 'name': name,
                               'form_user_email': None, 'user_information': user_information})
    context = {'detail_modal': True, 'users': users, 'form_user': form_user_detail, 'name': name,
               'form_user_email': form_user, 'user_information': user_information}
    return render(request, 'general_app/manage_users.html', context)


@login_required
def delete_record(request, pk):
    id_user = CertificateFile.objects.get(id=pk).hospital_id
    # print(User_Detail.objects.get(user_id=id_user).is_upload)
    User_Detail.objects.filter(user_id=id_user).update(is_upload=False)
    # print(User_Detail.objects.get(user_id=id_user).is_upload)
    CertificateFile.objects.filter(id=pk).delete()
    # User_Detail.objects.filter(user_id=request.user.id).update(is_upload=False)
    return HttpResponseRedirect(reverse('home'))


@login_required
def delete_user(request, name):
    id = User.objects.get(username=name).id
    try:
        User.objects.get(id=id).delete()
        return HttpResponseRedirect(reverse('manage_user'))
    except User.DoesNotExist:
        messages.error(request, 'User does not exist')
        return HttpResponseRedirect(reverse('manage_user'))


@login_required
def dashboard(request):
    data = {}
    check_box = None
    try:
        search = request.GET.getlist('search_users')
    except:
        search = None
    date_range_default_start = datetime.datetime(int(datetime.datetime.now().year) + 543, datetime.datetime.now().month,
                                                 datetime.datetime.now().day).strftime("%m/%d/%Y")  # for date_range
    date_range_default_end = datetime.datetime(int(datetime.datetime.now().year) + 543, datetime.datetime.now().month,
                                               datetime.datetime.now().day).strftime("%m/%d/%Y")  # for date_range
    # if 'daterange' in request.GET:
    try:
        date_range = str(request.GET['daterange']).split('-')
        date_range_default_start = date_range[0]
        date_range_default_end = date_range[1]
        date_start = datetime.date(int(str(date_range[0]).split('/')[2]) - 543, int(str(date_range[0]).split('/')[0]),
                                   int(str(date_range[0]).split('/')[1]))
        date_end = datetime.date(int(str(date_range[1]).split('/')[2]) - 543, int(str(date_range[1]).split('/')[0]),
                                 int(str(date_range[1]).split('/')[1]))
    except:
        date_start = datetime.date.today()
        date_end = datetime.date.today()
    if not 'search_users' in request.GET and not (date_start != date_end):
        data = fecth_report(User.objects.all())
    elif 'search_users' in request.GET and not (date_start != date_end):
        data = fecth_report(User.objects.filter(username__in=request.GET.getlist('search_users')))
    elif date_start != date_end and not 'search_users' in request.GET:
        # search = User.objects.filter(username__in=request.GET.getlist('search_users'))
        data = fecth_report(CertificateFile.objects.filter(create_date__range=[str(date_start), str(date_end)]))
    elif date_start != date_end and 'search_users' in request.GET:
        id = User.objects.filter(username__in=request.GET.getlist('search_users')).values_list('id')
        data = fecth_report(
            CertificateFile.objects.filter(hospital_id__in=id).filter(create_date__range=[date_start, date_end]))
    # if 'search_users' in request.GET :
    #     search = User.objects.filter(username__in=request.GET.getlist('search_users'))
    #     if 'daterange' in request.GET and (date_start != datetime.date.today() or date_end != datetime.date.today() ):
    #         search = users
    #
    # elif not 'search_users' in request.GET:
    #     data = fecth_report(User.objects.all())
    if 'is_upload' in request.GET:
        new_data = {}
        for obj in data:
            if data[obj]['upload_date'] != '':
                new_data[obj] = data[obj]
        data = new_data
        check_box = 'checked'
    if 'pdf' in request.GET:
        respone = create_pdf(data)
        return respone
    context = {
        'data': data,
        'users': User.objects.all(),
        'date_range_default_start': date_range_default_start,
        'date_range_default_end': date_range_default_end,
        'searched': search,
        'check_box': check_box
    }
    return render(request, 'general_app/dashboard.html', context)


@login_required
def test(request):
    return render(request, 'general_app/test.html', )


def fecth_report(obj):
    data = {}
    count = 0
    users = obj
    try:
        for user in users:
            user.id = user.hospital_id
    except:
        pass
    for user in users:
        if User_Detail.objects.get(user_id=user.id).is_upload:
            upload = CertificateFile.objects.filter(hospital_id=user.id).order_by('-create_date')[0]
            cert_id = upload.id
            count_download = upload.count_download
            upload = date_th(upload)[0]
        else:
            upload = ''
            count_download = ''
        data[count] = {'hospital': user, 'count_download': count_download,
                       'upload_date': upload}
        count += 1
    return data


def upload_certificate(request):
    try:
        verify_certificateform = Verify_CertificateForm(request.POST, request.FILES)
    except:
        verify_certificateform = Verify_CertificateForm()
    if request.method == "POST":
        if request.FILES:
            if verify_certificateform.is_valid():
                obj = verify_certificateform.save(commit=False)
                obj.user_create = request.user
                obj.save()
            return HttpResponseRedirect(reverse('upload_certificate'))
        elif 'cert_id' in request.POST:
            Verify_Certificatefile.objects.filter(pk=request.POST['cert_id']).update(editing_message=request.POST['editing_message'],user_create=request.user.username)
            return HttpResponseRedirect(reverse('upload_certificate'))
        elif 'delete_cert' in request.POST and request.POST['delete_cert'] != '':
            Verify_Certificatefile.objects.get(pk=request.POST['delete_cert_id']).delete()
            return HttpResponseRedirect(reverse('upload_certificate'))
        elif 'confirm_cert' in request.POST and request.POST['confirm_cert']:
            # Verify_Certificatefile.objects.get(pk=request.POST['delete_cert_id']).delete()
            certifi_form = CertificateForm(request.POST, request.FILES)
            if certifi_form.is_valid():
                certifi_form.save()
            return HttpResponseRedirect(reverse('upload_certificate'))
    verify_certificate_editing = Verify_Certificatefile.objects.filter(editing_message__isnull=False).exclude(
        editing_message__exact='')
    verify_certificate_confirm = Verify_Certificatefile.objects.filter(editing_message='')
    for index, file in enumerate(verify_certificate_editing):
        verify_certificate_editing[index].create_date = date_th(file)
    for index, file in enumerate(verify_certificate_confirm):
        verify_certificate_confirm[index].create_date = date_th(file)
    context = {
        'verify_certificateform': verify_certificateform,
        'verify_certificate_editing': verify_certificate_editing,
        'verify_certificate_confirm': verify_certificate_confirm,

    }
    return render(request, 'general_app/upload_certificate.html', context)

