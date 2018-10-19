from django.conf.urls import url
from django.contrib.auth.views import login, logout, password_reset, password_reset_done, password_reset_confirm, password_reset_complete
from . import views

app_name = 'account'

urlpatterns = [
    url(r'^profile/(?P<name>\w+)/$', views.ViewProfile, name='ProfileView'),
    url(r'^login/$', login, {'template_name': 'pages/2/login.html'}, name='login'),
    url(r'^logout/$', logout, {'template_name': 'pages/2/loggedout.html'}, name='logout'),
    url(r'^following/(?P<name>\w+)/unfollowed/$', views.unfollowUser, name='Unfollow'),
    url(r'^following/requests/(?P<name>\w+)/$', views.detailRequests, name='detailAcceptance'),
    url(r'^following/requests/(?P<name>\w+)/accept/$', views.editRequests, name='editAcceptance'),
    url(r'^following/requests/(?P<name>\w+)/decline/$', views.deleteRequests, name='deleteAcceptance'),
    url(r'^following/requests/(?P<name>\w+)/sent/$', views.makeRequests, name='makeAcceptance'),
    url(r'^following/requests/$', views.listRequests, name='listAcceptance'),
    url(r'^register/$', views.register, name='Register'),
    url(r'^delete/$', views.deleteProfile, name='DeleteProfile'),
    url(r'^profile-edit/$', views.updateProfile, name='update'),
    url(r'^change-password/$', views.change_password, name='change_password'),
    url(r'^reset-password/$', password_reset,  {'post_reset_redirect': 'account:password_reset_done'}, name='reset_password'),
    url(r'^reset-password/done/$', password_reset_done, name='password_reset_done'),
    #url(r'^reset-password/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', password_reset_confirm, {'post_reset_redirect': 'account:password_reset_complete'}, name='password_reset_confirm'),
    #url(r'^reset-password/complete/$', password_reset_complete, name='password_reset_complete'),
    #url(r'^requested/(?P<name>\w+)/$', views.makeRequest.as_view(), name='requested')
    url(r'^blocked/(?P<uuid>[\w]{8}(-[\w]{4}){3}-[\w]{12})/$', views.blockUser, name='blockUser'),
    url(r'unblocked/(?P<uuid>[\w]{8}(-[\w]{4}){3}-[\w]{12})/$', views.unblockUser, name='unblockUser'),
    url(r'preview/process/(?P<uuid>[\w]{8}(-[\w]{4}){3}-[\w]{12})/$', views.previewRemoveAdd, name='PreviewProcess'),
    #url(r'preview/remove/(?P<uuid>[\w]{8}(-[\w]{4}){3}-[\w]{12})/$', views.PreviewRemove, name='removePreview'),


#password reset
]
