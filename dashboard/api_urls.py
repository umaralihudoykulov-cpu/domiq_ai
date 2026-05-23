"""Dashboard - API URLs"""
from django.urls import path
from ai_design import api_views as ai_views
from estimates import api_views as est_views

urlpatterns = [
    path('v1/ai/generate-design/', ai_views.generate_design_api, name='api-generate-design'),
    path('v1/ai/chat/', ai_views.ai_chat_api, name='api-ai-chat'),
    path('v1/ai/electrical-analyze/', ai_views.electrical_analyze_api, name='api-electrical-analyze'),
    path('v1/estimates/calculate/', est_views.calculate_estimate_api, name='api-calculate-estimate'),
    path('v1/materials/calculate/', est_views.calculate_materials_api, name='api-calculate-materials'),
]
