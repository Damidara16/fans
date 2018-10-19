from django.contrib import admin
from .models import Content, Comment, Like

admin.site.register(Content)

admin.site.register(Comment)

admin.site.register(Like)
