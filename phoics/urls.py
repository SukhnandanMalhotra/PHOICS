from django.conf.urls import url, include
from django.contrib.auth import views as built_views
from django.contrib import admin
from django.contrib.auth.views import password_reset
from portal import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # this url is for admin page "/admin/"
    url(r'^admin/', admin.site.urls),
    # this is for user loggin in page "/"
    url(r'^$', views.front_page, name='front_page'),
    url(r'^phoics/', include('portal.urls')),
]


