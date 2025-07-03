from django.urls import path
from . import views

urlpatterns = [
    path('', views.templates_list, name='templates_list'),
    path('vyber-zariadeni/<int:template_id>/', views.equipment_select, name='equipment_select'),
]
