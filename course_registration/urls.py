

from django.urls import path, include
from django.contrib import admin
from registration.views import user_login  
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('registration/', include('registration.urls')),
    path('', user_login, name='login'), 
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('', include('registration.urls')),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)