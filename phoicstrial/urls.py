from django.conf.urls import url,include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from portal import views


urlpatterns = [
    # url for admin page
    url(r'^admin/', admin.site.urls),
    # url for initial page
    url(r'^$', views.home_page, name='home'),
    # url for login page
    url(r'^login/$', auth_views.login, {'template_name': 'portal/login.html'}, name='login'),
    # url for logout page and open login page
    url(r'^logout/$', auth_views.logout, {'next_page': 'login'}, name='logout'),
    #url for signup page
    url(r'^signup/$', views.sign_up, name='signup'),
    url(r'^account_activation_sent/$', views.account_activation_sent, name='account_activation_sent'),
     url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
         views.activate, name='activate'),
]