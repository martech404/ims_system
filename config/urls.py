from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from core import views as core_views  # Aliased as 'core_views'
from sales import views as sales_views  # Aliased as 'sales_views'

# ADMIN PANEL CUSTOMIZATION
admin.site.site_header = "Smart Inventory Admin"
admin.site.site_title = "Inventory Portal"
admin.site.index_title = "Welcome to the Backend"
admin.site.site_url = "/login"

urlpatterns = [
    path('admin/', admin.site.urls),

    # Core Views (Dashboard & Logout)
    path('', core_views.dashboard, name='dashboard'),
    path('logout/', core_views.custom_logout, name='logout'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),

    # Apps
    path('inventory/', include('inventory.urls')),
    path('sales/', include('sales.urls')),

    # Reports (Uses sales_views because that is where report_view is!)
    path('reports/', sales_views.report_view, name='sales_report'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)