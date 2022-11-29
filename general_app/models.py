from django.db import models
from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser, User


# Create your models here.
class User_Detail(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.TextField(blank=True)
    province = models.CharField(max_length=60, blank=True)
    ministry = models.CharField(max_length=60, blank=True)
    code = models.CharField(max_length=7, blank=True)
    cal_date = models.DateField(null=False)
    send_email = models.BooleanField(default=False)

    @property
    def email(self):
        return self.user.email

    @property
    def username(self):
        return self.user.username


class CertificateFile(models.Model):
    cert = models.FileField(upload_to='document %Y/%m/%d', null=False)
    hospital = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=False)
    create_date = models.DateField(auto_now_add=True, null=False)

    def __str__(self):
        return str(self.hospital)

    @property
    def username(self):
        return self.hospital.user.username

