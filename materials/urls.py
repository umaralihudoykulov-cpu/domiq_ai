"""Materials - URLs & Views"""
from django.urls import path
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

app_name = 'materials'

@login_required
def materials_view(request):
    return render(request, 'materials/calculator.html', {'page_title': 'Material Kalkulyator'})

urlpatterns = [
    path('', materials_view, name='calculator'),
]
