"""AI Design - Views"""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import AIDesign


@login_required
def ai_design_view(request):
    user_designs = AIDesign.objects.filter(user=request.user).order_by('-created_at')[:12]
    context = {
        'user_designs': user_designs,
        'page_title': 'AI Dizayn Studio — DomIQ Pro Max',
        'ai_limit': request.user.ai_limit,
        'ai_used': request.user.ai_requests_today,
    }
    return render(request, 'ai_design/studio.html', context)


@login_required
def gallery_view(request):
    designs = AIDesign.objects.filter(user=request.user, status='completed').order_by('-created_at')
    return render(request, 'ai_design/gallery.html', {'designs': designs, 'page_title': 'Mening Dizaynlarim'})
