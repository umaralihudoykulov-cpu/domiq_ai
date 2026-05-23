"""AI Design - URLs"""
from django.urls import path
from . import views

app_name = 'ai_design'

urlpatterns = [
    path('', views.ai_design_view, name='studio'),
    path('gallery/', views.gallery_view, name='gallery'),
]
