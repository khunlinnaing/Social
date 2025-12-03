
from django.contrib import admin
from project.models import *

@admin.register(Profile)
class ProfileAdminPage(admin.ModelAdmin):
    list_display= ('id',"profile")
    search_fields= ('user__username',)

@admin.register(Post)
class PostAdminPage(admin.ModelAdmin):
    list_display= ('id', "user", "description", "image", "video", "date")
    search_fields = ("user__name",)

@admin.register(Like)
class LikeAdminPage(admin.ModelAdmin):
    list_display= ('id', "user", "post", "is_like", "date")
    search_fields = ("user__name",)

@admin.register(Comment)
class CommentAdminPage(admin.ModelAdmin):
    list_display= ('id', "user", "post", "comment", "date")
    search_fields = ("user__name",)
