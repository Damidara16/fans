from django.conf.urls import url
from . import views

app_name='notif'

urlpatterns = [
    url(r'^edit/notification/$', views.editNotif, name='editNotif'),
]
