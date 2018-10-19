from django.conf.urls import url
from django.contrib.auth.views import login, logout
from . import views

app_name = 'content'

urlpatterns = [
    url(r'^detail/(?P<uuid>[\w]{8}(-[\w]{4}){3}-[\w]{12})/$', views.detailContent, name='detail'),
#post create
    url(r'^create/post/$', views.postCreate.as_view(), name='CreatePost'),
#video create
    url(r'^create/video/$', views.videoCreate.as_view(), name='CreateVideo'),
#tweet create
    url(r'^create/tweet/$', views.tweetCreate.as_view(), name='CreateTweet'),
#delete content
    url(r'^delete/(?P<uuid>[\w]{8}(-[\w]{4}){3}-[\w]{12})/$', views.deleteContent, name='DeleteContent'),
#delete comment
    url(r'^delete/comment/(?P<uuid>[\w]{8}(-[\w]{4}){3}-[\w]{12})/$', views.deleteComment, name='DeleteCOmment'),
#delete like
    url(r'^delete/like/(?P<uuid>[\w]{8}(-[\w]{4}){3}-[\w]{12})/$', views.deleteLike, name='DeleteLike'),
#comment create
    url(r'^create/comment/(?P<uuid>[\w]{8}(-[\w]{4}){3}-[\w]{12})/$', views.commentCreate, name='CreateComment'),
#comment create
    url(r'^create/like/(?P<uuid>[\w]{8}(-[\w]{4}){3}-[\w]{12})/$', views.likeCreate, name='CreateLike'),

]
