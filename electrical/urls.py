"""Electrical - URLs & Views"""
from django.urls import path
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

app_name = 'electrical'

@login_required
def electrical_view(request):
    return render(request, 'electrical/planner.html', {'page_title': 'Elektr Montaj AI'})

urlpatterns = [
    path('', electrical_view, name='planner'),
]
