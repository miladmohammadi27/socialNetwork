from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, OTPRequest


@admin.register(User)
class AppUserAdmin(UserAdmin):
    list_display = ("username", "first_name", "last_name", "is_staff", "nationality")

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Additional', {'classes': ('wide',), 'fields': ('nationality',)}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )


@admin.register(OTPRequest)
class OTPRequestAdmin(admin.ModelAdmin):
    list_display = ("request_id", "channel", "receiver", "password", "created")