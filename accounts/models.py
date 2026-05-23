"""Accounts - Custom User Model"""
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    PLAN_CHOICES = [
        ('free', 'Free'),
        ('pro', 'Pro'),
        ('premium', 'Premium'),
        ('business', 'Business'),
    ]
    
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    is_premium = models.BooleanField(default=False)
    plan = models.CharField(max_length=20, choices=PLAN_CHOICES, default='free')
    telegram_id = models.CharField(max_length=50, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    ai_requests_today = models.IntegerField(default=0)
    ai_requests_total = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Foydalanuvchi'
        verbose_name_plural = 'Foydalanuvchilar'

    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.plan})"

    @property
    def ai_limit(self):
        limits = {'free': 3, 'pro': 20, 'premium': 100, 'business': 999}
        return limits.get(self.plan, 3)

    @property
    def can_use_ai(self):
        return self.ai_requests_today < self.ai_limit

    def get_avatar_url(self):
        if self.avatar:
            return self.avatar.url
        return '/static/images/default-avatar.svg'
