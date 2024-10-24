from django.contrib import admin
from .models import Post, Comment, Like, Bookmark

admin.site.register(Like)
admin.site.register(Bookmark)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    autocomplete_fields = ['user']
    list_display = ['user', 'created', 'content']
    list_filter = ['user', 'created']
    search_fields = ['user', 'content']
    raw_id_fields = ['user']
    ordering = ['created', 'post']