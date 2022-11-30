from django.urls import path, include
from . import views
from users_app.views import login_user

urlpatterns = [
    path('', login_user, name='login'),
    path('users/', include('users_app.urls')),
    path('certificate/', views.certificate, name='certificate'),
    path('profile/', views.profile, name='profile'),
    path('configuration/', views.configuration, name='configuration'),
    path('Manage_users/', views.manage_user, name='manage_user'),
    path('Manage_users/<int:pk>', views.edit_user, name='edit_user')

]
