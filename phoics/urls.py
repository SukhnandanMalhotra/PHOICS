from django.conf.urls import url, include
from django.contrib.auth import views as built_views
from django.contrib import admin
from portal import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.home, name='home'),
    url(r'^login/$', built_views.login, {'template_name': 'portal/login.html'}, name='login'),
    url(r'^logout/$', built_views.logout, {'next_page': 'login'}, name='logout'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^account_activation_sent/$', views.account_activation_sent, name='account_activation_sent'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
    url(r'^front_page/$', views.front_page, name='front_page'),
    url(r'^forget_pass/$', views.forget_pass, name='forget_pass'),

]
