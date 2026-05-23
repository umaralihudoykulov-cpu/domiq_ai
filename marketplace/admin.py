"""Marketplace Admin"""
from django.contrib import admin
from .models import MasterProfile, Order, Review


@admin.register(MasterProfile)
class MasterProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'specialization', 'city', 'rating', 'is_verified', 'is_available', 'total_orders']
    list_filter = ['specialization', 'city', 'is_verified', 'is_available']
    search_fields = ['user__username', 'user__first_name', 'user__last_name']
    actions = ['verify_masters', 'unverify_masters']
    
    @admin.action(description='Tasdiqlash')
    def verify_masters(self, request, queryset):
        queryset.update(is_verified=True)
    
    @admin.action(description='Tasdiqni bekor qilish')
    def unverify_masters(self, request, queryset):
        queryset.update(is_verified=False)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'client', 'master', 'title', 'budget', 'status', 'created_at']
    list_filter = ['status']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['client', 'master', 'rating', 'created_at']
    list_filter = ['rating']
