from django.db import models
from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser, User


# Create your models here
class CertificateFile(models.Model):
    cert = models.FileField(upload_to='%Y/')
    hospital = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=False)
    create_date = models.DateField(auto_now_add=True, null=False)
    count_download = models.IntegerField(null=True, default=0)

    def __str__(self):
        return str(self.hospital)

    @property
    def username(self):
        return self.hospital.user.username


class Configuration(models.Model):
    delete_date = models.IntegerField(default=3)
    send_mail_date = models.IntegerField(default=-2)
    sender_mail = models.EmailField(null=False)
    sender_mail_status = models.BooleanField(null=False, default=0)
    delete_date_status = models.BooleanField(null=False, default=0)


class Province(models.Model):
    province = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return str(self.province)


class Ministry(models.Model):
    ministry = models.CharField(max_length=60, null=True, blank=True)

    def __str__(self):
        return str(self.ministry)


class User_Detail(models.Model):
    position = models.CharField(max_length=50, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.TextField(null=True, blank=True)
    province = models.ForeignKey(Province, on_delete=models.SET_NULL, null=True, blank=True)
    ministry = models.ForeignKey(Ministry, on_delete=models.SET_NULL, null=True, blank=True)
    code = models.CharField(max_length=7, null=True, blank=True)
    cal_date = models.DateField(null=True, blank=True)
    send_email = models.BooleanField(null=True, blank=True)
    is_upload = models.BooleanField(default=0)  # check upload for ceating PDF
    number = models.CharField(max_length=10,null=True)

    @property
    def email(self):
        return self.user.email

    @property
    def username(self):
        return self.user.username
