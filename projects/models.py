"""Projects - Core Project Models"""
from django.db import models
from django.conf import settings


class Project(models.Model):
    HOME_TYPES = [
        ('apartment', 'Kvartira'),
        ('house', 'Uy'),
        ('studio', 'Studiya'),
        ('villa', 'Villa'),
        ('office', 'Ofis'),
        ('commercial', 'Tijorat'),
    ]
    REPAIR_TYPES = [
        ('cosmetic', 'Kosmetik remont'),
        ('euro', 'Evro remont'),
        ('design', 'Dizayn remont'),
        ('premium', 'Premium remont'),
        ('full', 'Kapital remont'),
    ]
    STATUS_CHOICES = [
        ('planning', 'Rejalashtirilmoqda'),
        ('in_progress', 'Jarayonda'),
        ('completed', 'Yakunlangan'),
        ('on_hold', 'Kutmoqda'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='projects')
    title = models.CharField(max_length=200)
    home_type = models.CharField(max_length=20, choices=HOME_TYPES)
    area = models.FloatField(help_text='Kvadrat metr')
    rooms = models.IntegerField(default=1)
    bathrooms = models.IntegerField(default=1)
    floors = models.IntegerField(default=1)
    repair_type = models.CharField(max_length=20, choices=REPAIR_TYPES, default='euro')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='planning')
    address = models.CharField(max_length=300, blank=True)
    description = models.TextField(blank=True)
    budget = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    has_smart_home = models.BooleanField(default=False)
    floor_plan = models.ImageField(upload_to='floor_plans/', blank=True, null=True)
    progress = models.IntegerField(default=0, help_text='0-100%')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Loyiha'
        verbose_name_plural = 'Loyihalar'

    def __str__(self):
        return f"{self.title} - {self.user.username}"

    def get_total_cost(self):
        estimates = self.estimates.all()
        if estimates.exists():
            return sum(e.total_cost for e in estimates)
        return 0
