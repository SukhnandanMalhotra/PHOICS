from django.conf.urls import url
from . import views

app_name='polls'
urlpatterns = [
    url(r'^$', views.home_page, name='starting'),
    url(r'^signup/$', views.sign_up, name='signup'),

]
