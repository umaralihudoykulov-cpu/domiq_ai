"""Dashboard - URLs"""
from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('pricing/', views.pricing_view, name='pricing'),
    path('about/', views.about_view, name='about'),
    path('contact/', views.contact_view, name='contact'),
]
