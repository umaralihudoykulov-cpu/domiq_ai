"""Projects Admin"""
from django.contrib import admin
from .models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'home_type', 'area', 'repair_type', 'status', 'created_at']
    list_filter = ['home_type', 'repair_type', 'status', 'has_smart_home']
    search_fields = ['title', 'user__username', 'address']
    date_hierarchy = 'created_at'
