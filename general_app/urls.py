from django.urls import path, include
from . import views
from users_app.views import login_user
from django.conf import settings
from django.conf.urls.static import static
# from django.views.i18n import JavaScriptCatalog

urlpatterns = [
    path('', login_user, name='login'),
    path('users/', include('users_app.urls')),
    path('home/', views.home, name='home'),
    path('profile/', views.profile, name='profile'),
    path('configuration/', views.configuration, name='configuration'),
    path('Manage_users/', views.manage_user, name='manage_user'),
    path('Manage_users/<int:pk>/', views.edit_user, name='edit_user'),
    path('home/pdf/',views.generate_pdf, name='pdf')

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
