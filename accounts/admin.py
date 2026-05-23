"""Admin configurations"""
from django.contrib import admin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'plan', 'is_premium', 'ai_requests_total', 'date_joined']
    list_filter = ['plan', 'is_premium', 'is_staff']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    readonly_fields = ['ai_requests_today', 'ai_requests_total', 'date_joined']
    fieldsets = (
        ('Asosiy', {'fields': ('username', 'email', 'first_name', 'last_name', 'password')}),
        ('Premium', {'fields': ('plan', 'is_premium', 'ai_requests_today', 'ai_requests_total')}),
        ('Qo\'shimcha', {'fields': ('phone_number', 'telegram_id', 'avatar', 'bio', 'city')}),
        ('Huquqlar', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Vaqtlar', {'fields': ('date_joined', 'last_login')}),
    )
