"""Dashboard - Main Views"""
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count, DecimalField
from django.db.models.functions import Coalesce
from decimal import Decimal
from projects.models import Project
from ai_design.models import AIDesign
from estimates.models import Estimate


def home_view(request):
    """Public Homepage"""
    context = {
        'page_title': 'DomIQ Pro Max — AI Remont Platformasi',
    }
    return render(request, 'home/index.html', context)


@login_required
def dashboard_view(request):
    """Main User Dashboard"""
    user = request.user
    projects = Project.objects.filter(user=user)
    designs = AIDesign.objects.filter(user=user).order_by('-created_at')[:6]
    
    # Stats
    total_projects = projects.count()
    active_projects = projects.filter(status='in_progress').count()
    completed_projects = projects.filter(status='completed').count()
    
    # Total spent — null-safe aggregation
    total_spent = Estimate.objects.filter(user=user).aggregate(
        material=Coalesce(Sum('material_cost'), Decimal('0'), output_field=DecimalField()),
        labor=Coalesce(Sum('labor_cost'), Decimal('0'), output_field=DecimalField()),
        electrical=Coalesce(Sum('electrical_cost'), Decimal('0'), output_field=DecimalField()),
        furniture=Coalesce(Sum('furniture_cost'), Decimal('0'), output_field=DecimalField()),
        design=Coalesce(Sum('design_cost'), Decimal('0'), output_field=DecimalField()),
        smart=Coalesce(Sum('smart_home_cost'), Decimal('0'), output_field=DecimalField()),
    )
    total_spent = sum(total_spent.values())
    
    context = {
        'projects': projects[:5],
        'recent_designs': designs,
        'total_projects': total_projects,
        'active_projects': active_projects,
        'completed_projects': completed_projects,
        'total_spent': total_spent,
        'ai_limit': user.ai_limit,
        'ai_used': user.ai_requests_today,
        'page_title': 'Dashboard — DomIQ Pro Max',
    }
    return render(request, 'dashboard/home.html', context)


def pricing_view(request):
    return render(request, 'home/pricing.html', {'page_title': 'Narxlar — DomIQ Pro Max'})


def about_view(request):
    return render(request, 'home/about.html', {'page_title': 'Biz Haqimizda — DomIQ Pro Max'})


def contact_view(request):
    return render(request, 'home/contact.html', {'page_title': 'Aloqa — DomIQ Pro Max'})
