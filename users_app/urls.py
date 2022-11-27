from django.urls import path, include
from . import views

urlpatterns = [
    path('login/', views.login_user, name='login'),
    path('',include('django.contrib.auth.urls')),
]
