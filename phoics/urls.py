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

]