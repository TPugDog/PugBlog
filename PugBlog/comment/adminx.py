from django.contrib import admin
from .models import Comment
import xadmin
from PugBlog.base_admin import BaseOwnerAdmin
from itertools import chain
# Register your models here.

@xadmin.sites.register(Comment)
class CommentAdmin(BaseOwnerAdmin):
    list_display = ('target', 'nickname', 'content', 'website','email', 'created_time')

    def get_list_queryset(self):
        all_comment = Comment.objects.none()
        postid_list = []
        comment_list = []
        request = self.request
        posts_list = Comment.get_user_posts(request)
        qs = super(BaseOwnerAdmin, self).get_list_queryset()
        for i in posts_list:
            postid_list.append('/post/'+str(i))
        for k in postid_list:
            comment_list.append(qs.filter(target = k))
        for i in comment_list:
            all_comment = all_comment | i
        comment_list = chain(all_comment)
        return comment_list

    # def get_list_queryset(self):
    #     request = self.request
    #     qs = super(BaseOwnerAdmin, self).get_list_queryset()
    #     return qs.filter(target="'/post/'+ str(3)")