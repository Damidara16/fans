from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
import uuid

class Content(models.Model):
    contents = (('Post', 'Post'),('Video', 'Video'),('Tweet', 'Tweet'))
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    views = models.IntegerField(default=0)
    thumbnail = models.FileField(null=True, blank=True)
    file = models.FileField(null=True, blank=True)
    caption = models.CharField(max_length=255, null=True)
    typeContent = models.CharField(max_length=5, choices=contents)
    preview = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse('content:detail', kwargs={'uuid':self.uuid})

    def __str__(self):
        return self.typeContent + ' ' + self.user.username

    def likeCount(self):
        return self.like_set.all().count()

    def commentCount(self):
        return self.comment_set.all().count()

#split the model through forms exclude(), and through views
'''
    class Meta:
        abstract = True

class Post(Content):
    file = models.FileField()
    description = models.CharField(max_length=255)

class Video(Content):
    file = models.FileField()
    description = models.CharField(max_length=255)

class Tweet(Content):
    content = models.CharField(max_length=200)
'''
class SubContent(models.Model):
    ParentContent = models.ForeignKey(Content, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timeStamp = models.DateTimeField(auto_now_add=True)
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True

class Comment(SubContent):
    comment = models.CharField(max_length=200)

class Like(SubContent):
    #to get like count on a content, just return the count, there's a function for this called likeCount()
    like = models.BooleanField(default=True)
