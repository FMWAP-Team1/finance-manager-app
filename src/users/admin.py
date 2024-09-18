from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


class CustomUserAdmin(BaseUserAdmin):
    list_display = ('email', 'name', 'nickname', 'phone_number', 'is_admin', 'is_active')
    list_display_links = ('email',)
    list_filter = ('is_admin', 'is_active')
    search_fields = ('email', 'nickname', 'phone_number')
    readonly_fields = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('name', 'nickname', 'phone_number')}),
        ('Permissions', {'fields': ('is_admin', 'is_active')}),
    )
    ordering = ('email',)


admin.site.register(User, CustomUserAdmin)
