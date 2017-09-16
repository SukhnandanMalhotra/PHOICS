from django.conf.urls import url, include
from django.contrib.auth import views as built_views
from django.contrib import admin
from portal import views

urlpatterns = [
    # this url is for admin page "/admin/"
    url(r'^admin/', admin.site.urls),
    # this is for user loggin in page "/"
    url(r'^$', views.home, name='home'),
    # this is for login page "/login"
    url(r'^login/$', built_views.login, {'template_name': 'portal/login.html'}, name='login'),
    # for logout but open login page
    url(r'^logout/$', built_views.logout, {'next_page': 'login'}, name='logout'),
    # signup page "/signup/"
    url(r'^signup/$', views.signup, name='signup'),
    # page after email send for verification "/account_activation_sent/"
    url(r'^account_activation_sent/$', views.account_activation_sent, name='account_activation_sent'),
    # a link that send to user in email to activate your phoics account
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
    # for front page "/front_page"
    url(r'^front_page/$', views.front_page, name='front_page'),
    # if we 
    url(r'^forget_pass/$', views.forget_pass, name='forget_pass'),

]
