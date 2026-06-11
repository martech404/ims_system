from django.urls import path
from . import views

urlpatterns = [
    path('pos/', views.pos_view, name='pos_view'),
   path('pos/', views.pos_view, name='pos_view'),
    path('reports/', views.report_view, name='sales_report'),
    path('receipt/<int:sale_id>/', views.receipt_view, name='receipt'),
    path('reports/', views.report_view, name='sales_report'),
    path('receipt/<int:sale_id>/', views.receipt_view, name='receipt'),
]