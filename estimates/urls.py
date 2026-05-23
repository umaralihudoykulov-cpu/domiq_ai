"""Estimates - URLs & Views"""
from django.urls import path
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

app_name = 'estimates'

@login_required
def estimate_view(request):
    return render(request, 'estimates/calculator.html', {'page_title': 'Smeta Kalkulyator'})

urlpatterns = [
    path('', estimate_view, name='calculator'),
]
