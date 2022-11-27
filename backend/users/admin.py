from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


class UserAdminConfig(UserAdmin):
    search_fields = ('username',)
    ordering = ('username',)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_superuser', 'date_joined')


admin.site.register(User, UserAdminConfig)