"""DomIQ Pro Max - URL Configuration"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('dashboard.urls')),
    path('auth/', include('accounts.urls')),
    path('projects/', include('projects.urls')),
    path('ai-design/', include('ai_design.urls')),
    path('electrical/', include('electrical.urls')),
    path('estimates/', include('estimates.urls')),
    path('marketplace/', include('marketplace.urls')),
    path('materials/', include('materials.urls')),
    path('smart-home/', include('smart_home.urls')),
    path('api/', include('dashboard.api_urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Custom Admin
admin.site.site_header = "DomIQ Pro Max Admin"
admin.site.site_title = "DomIQ Admin"
admin.site.index_title = "Boshqaruv Paneli"
