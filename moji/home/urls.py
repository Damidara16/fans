from django.conf.urls import url
from . import views

app_name = 'home'

urlpatterns = [
    url(r'^$', views.index ,name='home'),
    url(r'^bug/$', views.emailReport.as_view(), name='bug'),
    url(r'^search/$', views.SearchUser, name='search'),
    url(r'^discover/$', views.discoverView, name='discovered'),
    url(r'^discover/(?P<genre>\w+)/$', views.discoverGenre, name='genre'),
    url(r'^about/$', views.aboutUs, name='about'),
    url(r'^how-we-work/$', views.Hww, name='hww'),
    url(r'^join/$', views.Join, name='join'),

]
