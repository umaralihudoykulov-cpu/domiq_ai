"""Marketplace - Master/Specialist Models"""
from django.db import models
from django.conf import settings


class MasterProfile(models.Model):
    SPECIALIZATION_CHOICES = [
        ('electrician', 'Elektrik'),
        ('designer', 'Dizayner'),
        ('plumber', 'Santexnik'),
        ('renovator', 'Remontchi'),
        ('carpenter', 'Mebelsoz'),
        ('smart_home', 'Smart-home ustasi'),
        ('painter', 'Bo\'yoqchi'),
        ('tiler', 'Kafelchi'),
    ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='master_profile')
    specialization = models.CharField(max_length=20, choices=SPECIALIZATION_CHOICES)
    experience_years = models.IntegerField(default=1)
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2, default=50000)
    bio = models.TextField()
    portfolio_images = models.JSONField(default=list)
    phone = models.CharField(max_length=20)
    telegram = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, default='Toshkent')
    is_verified = models.BooleanField(default=False)
    is_available = models.BooleanField(default=True)
    rating = models.FloatField(default=0)
    total_reviews = models.IntegerField(default=0)
    total_orders = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Usta Profil'

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.get_specialization_display()}"


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Kutmoqda'),
        ('accepted', 'Qabul qilindi'),
        ('in_progress', 'Bajarilmoqda'),
        ('completed', 'Yakunlandi'),
        ('cancelled', 'Bekor qilindi'),
    ]

    client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='client_orders')
    master = models.ForeignKey(MasterProfile, on_delete=models.CASCADE, related_name='master_orders')
    project = models.ForeignKey('projects.Project', on_delete=models.SET_NULL, null=True, blank=True)
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    budget = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order #{self.pk} - {self.master}"


class Review(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='review')
    client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    master = models.ForeignKey(MasterProfile, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review {self.rating}★ for {self.master}"
