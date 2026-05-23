"""Estimates - Cost Estimation Models"""
from django.db import models
from django.conf import settings


class Estimate(models.Model):
    project = models.ForeignKey('projects.Project', on_delete=models.CASCADE, related_name='estimates')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='estimates')
    title = models.CharField(max_length=200, default='Smeta')
    
    # Costs
    labor_cost = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    material_cost = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    electrical_cost = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    furniture_cost = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    design_cost = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    smart_home_cost = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    other_cost = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    
    # Details
    items = models.JSONField(default=list)
    notes = models.TextField(blank=True)
    ai_generated = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Smeta'
        verbose_name_plural = 'Smetalar'

    @property
    def total_cost(self):
        return (self.labor_cost + self.material_cost + self.electrical_cost +
                self.furniture_cost + self.design_cost + self.smart_home_cost + self.other_cost)

    def __str__(self):
        return f"{self.title} - {self.total_cost:,.0f} so'm"


class EstimateItem(models.Model):
    CATEGORY_CHOICES = [
        ('labor', 'Ish haqi'),
        ('material', 'Material'),
        ('electrical', 'Elektr'),
        ('furniture', 'Mebel'),
        ('plumbing', 'Santexnika'),
        ('smart_home', 'Smart Home'),
        ('other', 'Boshqa'),
    ]
    
    estimate = models.ForeignKey(Estimate, on_delete=models.CASCADE, related_name='estimate_items')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    name = models.CharField(max_length=200)
    unit = models.CharField(max_length=20, default='dona')
    quantity = models.FloatField(default=1)
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)
    
    @property
    def total_price(self):
        return self.quantity * self.unit_price

    def __str__(self):
        return f"{self.name} x{self.quantity}"
