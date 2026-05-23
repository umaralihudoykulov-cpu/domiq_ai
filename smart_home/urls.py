"""Smart Home - URLs & Views"""
from django.urls import path
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

app_name = 'smart_home'

@login_required
def smart_home_view(request):
    return render(request, 'smart_home/dashboard.html', {'page_title': 'Smart Home — DomIQ Pro Max'})

urlpatterns = [
    path('', smart_home_view, name='dashboard'),
]
