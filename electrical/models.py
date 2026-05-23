"""Electrical - Electrical Planning Models"""
from django.db import models
from django.conf import settings


class ElectricalPlan(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Kutmoqda'),
        ('analyzing', 'Tahlil qilinmoqda'),
        ('completed', 'Tayyor'),
        ('failed', 'Xato'),
    ]

    project = models.ForeignKey('projects.Project', on_delete=models.CASCADE, related_name='electrical_plans', null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='electrical_plans')
    
    # Input
    floor_plan_image = models.ImageField(upload_to='electrical/', blank=True, null=True)
    area = models.FloatField(default=50)
    rooms = models.IntegerField(default=3)
    has_smart_home = models.BooleanField(default=False)
    
    # AI Analysis Results
    sockets_count = models.IntegerField(default=0)
    switches_count = models.IntegerField(default=0)
    lights_count = models.IntegerField(default=0)
    cable_length = models.FloatField(default=0)
    circuit_breakers = models.IntegerField(default=0)
    
    # Detailed JSON results
    socket_positions = models.JSONField(default=list)
    switch_positions = models.JSONField(default=list)
    light_positions = models.JSONField(default=list)
    smart_home_devices = models.JSONField(default=list)
    
    ai_analysis = models.TextField(blank=True)
    recommendations = models.JSONField(default=list)
    estimated_cost = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Elektr Reja'
        verbose_name_plural = 'Elektr Rejalar'

    def __str__(self):
        return f"Electrical Plan #{self.pk}"
