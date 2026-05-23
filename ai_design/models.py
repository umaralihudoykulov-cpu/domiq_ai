"""AI Design - AI Generated Designs"""
from django.db import models
from django.conf import settings


class DesignStyle(models.Model):
    name = models.CharField(max_length=100)
    name_uz = models.CharField(max_length=100)
    description = models.TextField()
    preview_image = models.ImageField(upload_to='styles/', blank=True)
    prompt_template = models.TextField(help_text='AI prompt template')
    
    def __str__(self):
        return self.name_uz


class AIDesign(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Kutmoqda'),
        ('processing', 'Jarayonda'),
        ('completed', 'Tayyor'),
        ('failed', 'Xato'),
    ]
    
    project = models.ForeignKey('projects.Project', on_delete=models.CASCADE, related_name='designs', null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='designs')
    
    # Input
    room_type = models.CharField(max_length=50, default='living_room')
    style = models.CharField(max_length=50, default='modern')
    area = models.FloatField(default=30)
    color_scheme = models.CharField(max_length=100, default='neutral')
    budget_level = models.CharField(max_length=20, default='medium')
    custom_prompt = models.TextField(blank=True)
    
    # Output
    image = models.ImageField(upload_to='ai_designs/', blank=True, null=True)
    image_url = models.URLField(blank=True)
    ai_response = models.TextField(blank=True)
    color_palette = models.JSONField(default=list)
    furniture_suggestions = models.JSONField(default=list)
    material_suggestions = models.JSONField(default=list)
    
    # Meta
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    generation_time = models.FloatField(null=True, blank=True)
    prompt_used = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'AI Dizayn'

    def __str__(self):
        return f"Design #{self.pk} - {self.style} by {self.user.username}"


class AIChat(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='ai_chats')
    project = models.ForeignKey('projects.Project', on_delete=models.SET_NULL, null=True, blank=True)
    session_id = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Chat {self.session_id}"


class AIChatMessage(models.Model):
    chat = models.ForeignKey(AIChat, on_delete=models.CASCADE, related_name='messages')
    role = models.CharField(max_length=20, choices=[('user', 'User'), ('assistant', 'Assistant')])
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
