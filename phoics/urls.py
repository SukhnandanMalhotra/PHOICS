from django.conf.urls import url, include
from django.contrib import admin
from portal import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    # this url is for admin page "/admin/"
    url(r'^admin/', admin.site.urls),
    # this is for user loggin in page "/"
    url(r'^$', views.front_page, name='front_page'),
    url(r'^phoics/', include('portal.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = views.error404
handler400 = views.error400
handler500 = views.error500
handler403 = views.error403
