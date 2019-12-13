from django.contrib import admin
from .models import Content, Comment, Like

class ContentAdmin(admin.ModelAdmin):
    list_display = ('user', 'typeContent', 'date', 'uuid')

    #def userinfo(self, obj):
        #return obj.user.username

    def queryset(self, request):
        qs = super(ContentAdmin, self).get_queryset(request)
        qs = qs.order_by('date')
        return qs

class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'repliedUser', 'contentid')

    def repliedUser(self, obj):
        return obj.ParentContent.user.username

    def contentid(self, obj):
        return obj.ParentContent.uuid

#admin.site.register(Content, ContentAdmin)

admin.site.register(Comment, CommentAdmin)

admin.site.register(Like)
