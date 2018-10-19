from django.conf.urls import url
from . import views

app_name = 'product'

urlpatterns = [
    url(r'^create/points/$', views.SetPoints, name='SetPoints'),
    url(r'^tipcreation/(?P<name>\w+)/$', views.SendTip, name='SendTip'),
    url(r'^sub/(?P<uuid>[\w]{8}(-[\w]{4}){3}-[\w]{12})/$', views.tempSub, name='tempSub'),
    url(r'^subscription/(?P<uuid>[\w]{8}(-[\w]{4}){3}-[\w]{12})/$', views.addSub, name='addSub'),
    url(r'^create/plan/$', views.CreatePlan.as_view(), name='CreatePlan'),
    url(r'^update/points/$', views.PointsUpdate.as_view(), name='PointsUpdate'),
    url(r'^cancellation/(?P<name>\w+)/$', views.cancelSub, name='cancelSub'),
    url(r'^removed/$', views.removeUser, name='removeUser'),
    url(r'^payout-account/$', views.viewStripe, name='stripeview'),
    #url(r'^success/$', views.success, name='success')

]
#7dfc7774-9345-4622-938f-c83a08edb4f5
