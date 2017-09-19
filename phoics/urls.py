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
    url(r'^$', views.home, name='profile'),
    #
    url(r'^upload/$', views.model_form_upload, name='model_form_upload'),
    #
    url(r'^newsfeed/$', views.newsfeed, name='newsfeed'),
    # this is for login page "/login"
    url(r'^login/$', built_views.login, {'template_name': 'portal/login.html'}, name='login'),
    # for logout but open login page
    url(r'^logout/$', built_views.logout, {'next_page': 'front_page'}, name='logout'),
    # signup page "/signup/"
    url(r'^signup/$', views.signup, name='signup'),
    # page after email send for verification "/account_activation_sent/"
    url(r'^account_activation_sent/$', views.account_activation_sent, name='account_activation_sent'),
    # a link that send to user in email to activate your phoics account
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
    # for front page "/front_page"
    url(r'^front_page/$', views.front_page, name='front_page'),
    url(r'^password_reset/$', built_views.password_reset, name='password_reset'),
    url(r'^password_reset/done/$', built_views.password_reset_done, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        built_views.password_reset_confirm, name='password_reset_confirm'),
    url(r'^reset/done/$', built_views.password_reset_complete, name='password_reset_complete'),

    # if user forget password then go "/forget_pass/"
    # url(r'^forget_pass/$', views.forget_pass, name='forget_pass'),
    # url(r'^enter_otp/$', views.enter_otp, name='enter_otp'),
    # url(r'^reset_pass/$', views.reset_pass, name='reset_pass'),
    # url(r'^password_reset/$', password_reset, {'template_name': 'portal/reset_password_form.html'}, name='reset_password'),
   ]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
