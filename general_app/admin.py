from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CertificateFile, User_Detail
from django.contrib.auth.models import User

# Register your models here.
admin.site.register(CertificateFile)
admin.site.register(User_Detail)


class EmployeeInline(admin.StackedInline):
    model = User_Detail
    can_delete = False
    verbose_name_plural = 'employee'


# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = [EmployeeInline]


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
