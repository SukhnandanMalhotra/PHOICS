from django.conf.urls import url, include
from django.contrib.auth import views as built_views
from django.contrib import admin
from portal import views
from django.contrib.auth.views import password_reset
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # this url is for admin page "/admin/"
    url(r'^admin/', admin.site.urls),
    # this is for user loggin in page "/"
    url(r'^', include('portal.urls')),

   ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
