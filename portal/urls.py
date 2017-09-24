from django.conf.urls import url, include
from django.contrib.auth import views as built_views
from django.contrib import admin
from portal import views
from django.contrib.auth.views import password_reset
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^$', views.home, name='profile'),
    url(r'^upload/$', views.model_form_upload, name='model_form_upload'),

    url(r'^newsfeed/$', views.newsfeed, name='newsfeed'),
    # this is for login page "/login"
    url(r'^login/$', built_views.login, {'template_name': 'portal/login.html'}, name='login'),
    # for logout but open login page
    url(r'^logout/$', built_views.logout, {'next_page': 'front_page'}, name='logout'),
    # signup page "/signup/"
    url(r'^information/$', views.user_info, name="user_info"),
    url(r'^signup/$', views.signup, name='signup'),
    # page after email send for verification "/account_activation_sent/"
    #url(r'^account_activation_sent/$', views.account_activation_sent, name='account_activation_sent'),
    # a link that send to user in email to activate your phoics account
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
    # for front page "/front_page"
    url(r'^front_page/$', views.front_page, name='front_page'),
    url(r'^password_reset/$', password_reset, {
        'template_name': 'forget/password_reset_form.html'}, name='password_reset'),

    url(r'^password_reset/done/$', built_views.password_reset_done, {
        'template_name': 'forget/password_reset_done.html'}, name='password_reset_done'),

    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        built_views.password_reset_confirm, {
            'template_name': 'forget/password_reset_confirm.html'}, name='password_reset_confirm'),

    url(r'^reset/done/$', built_views.password_reset_complete, {
        'template_name': 'forget/password_reset_complete.html'}, name='password_reset_complete'),

    url(r'^edit/(?P<pk>\d+)$', views.Doc_update, name='Doc_edit'),

    url(r'^delete/(?P<pk>\d+)$', views.Doc_delete, name='Doc_delete'),
   ]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
