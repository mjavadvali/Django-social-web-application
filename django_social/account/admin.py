from django.contrib import admin
from .models import User, UserFollowing

@admin.register(User)
class PostAdmin(admin.ModelAdmin):
    search_fields = ['username']


admin.site.register(UserFollowing)