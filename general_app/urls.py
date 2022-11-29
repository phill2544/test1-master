from django.urls import path, include
from . import views
from users_app.views import login_user

urlpatterns = [
    path('', login_user, name='login'),
    path('users/', include('users_app.urls')),
    path('certificate/', views.certificate, name='certificate'),
    path('profile/', views.profile, name='profile'),
    path('upload_certificate/', views.upload_cert, name='upload_cert'),
    path('configuration/', views.configuration, name='configuration'),

]
