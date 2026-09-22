from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, Post, Comment, Like, Follow


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Profile', {'fields': ('bio', 'avatar_url')}),
    )


admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Follow)
