from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Follow, User


class UserAdminConfig(UserAdmin):
    search_fields = ('username', 'email')
    list_display = ('username', 'email', 'first_name',
                    'last_name', 'is_superuser', 'date_joined')


class FollowAdminConfig(admin.ModelAdmin):
    list_display = ('author', 'user')


admin.site.register(User, UserAdminConfig)
admin.site.register(Follow, FollowAdminConfig)
