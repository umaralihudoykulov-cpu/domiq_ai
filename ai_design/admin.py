"""AI Design Admin"""
from django.contrib import admin
from .models import AIDesign, AIChat, AIChatMessage, DesignStyle


@admin.register(AIDesign)
class AIDesignAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'style', 'room_type', 'area', 'status', 'created_at']
    list_filter = ['style', 'status', 'room_type']
    search_fields = ['user__username']
    readonly_fields = ['prompt_used', 'generation_time']


@admin.register(DesignStyle)
class DesignStyleAdmin(admin.ModelAdmin):
    list_display = ['name', 'name_uz']


admin.site.register(AIChat)
admin.site.register(AIChatMessage)
