from django.conf.urls import url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from portal import views



urlpatterns = [
    url(r'^$', views.home, name='profile'),
    url(r'^upload/$', views.model_form_upload, name='model_form_upload'),
    url(r'^newsfeed/$', views.newsfeed, name='newsfeed'),
    url(r'^edit/(?P<pk>\d+)$', views.Doc_update, name='Doc_edit'),
    url(r'^delete/(?P<pk>\d+)$', views.Doc_delete, name='Doc_delete'),
    url(r'^admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
