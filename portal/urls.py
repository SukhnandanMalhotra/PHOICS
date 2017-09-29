from django.conf.urls import url, include
from django.contrib.auth import views as built_views
from django.contrib import admin
from portal import views
from django.contrib.auth.views import password_reset
from django.conf import settings
from django.conf.urls.static import static
# from django_filters.views import FilterView
# from portal.filters import UserFilter

urlpatterns = [
    url(r'^$', views.home, name='profile'),

    url(r'^upload/$', views.model_form_upload, name='model_form_upload'),

    url(r'^newsfeed/$', views.newsfeed, name='newsfeed'),

    url(r'^login/$', built_views.login, {'template_name': 'portal/login.html'}, name='login'),

    url(r'^logout/$', built_views.logout, {'next_page': 'login'}, name='logout'),

    url(r'^information/$', views.user_info, name="user_info"),

    url(r'^signup/$', views.signup, name='signup'),

    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),

    url(r'^frontpage/$', views.front_page, name='front_page'),

    url(r'^passwordreset/$', password_reset, {
        'template_name': 'forget/password_reset_form.html'}, name='password_reset'),

    url(r'^passwordreset/done/$', built_views.password_reset_done, {
        'template_name': 'forget/password_reset_done.html'}, name='password_reset_done'),

    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        built_views.password_reset_confirm, {
            'template_name': 'forget/password_reset_confirm.html'}, name='password_reset_confirm'),

    url(r'^reset/done/$', built_views.password_reset_complete, {
        'template_name': 'forget/password_reset_complete.html'}, name='password_reset_complete'),

    url(r'^edit/(?P<pk>\d+)$', views.doc_update, name='Doc_edit'),

    url(r'^delete/(?P<pk>\d+)$', views.doc_delete, name='Doc_delete'),

    # url(r'^reset/(?P<pk>\d+)$', views.Doc_reset, name='Doc_reset'),
    # url(r'^search/$', FilterView.as_view(filterset_class=UserFilter, template_name='portal/user_list.html'), name='search'),

   ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
