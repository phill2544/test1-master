from django.urls import path, include
from . import views

urlpatterns = [
    path('login/', views.login_user, name='login'),
    path('', include('django.contrib.auth.urls')),
    # path('change_password/', views.change_password, name='change_password')
]
