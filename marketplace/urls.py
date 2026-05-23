"""Marketplace - URLs & Views"""
from django.urls import path
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

app_name = 'marketplace'

def marketplace_view(request):
    from marketplace.models import MasterProfile
    masters = MasterProfile.objects.filter(is_verified=True, is_available=True)
    specialization = request.GET.get('spec', '')
    if specialization:
        masters = masters.filter(specialization=specialization)
    return render(request, 'marketplace/index.html', {
        'masters': masters,
        'page_title': 'Usta Bozori — DomIQ Pro Max',
        'selected_spec': specialization,
    })

urlpatterns = [
    path('', marketplace_view, name='index'),
]
