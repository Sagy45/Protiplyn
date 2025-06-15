"""
URL configuration for protiplyn project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from viewer import views
from viewer.views import *
from equipment.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('country/', views.country_detail_full, name='country_detail_full'),
    path('', EquipmentTypeListView.as_view(), name='equipmenttype_list'),
    path('add/', EquipmentTypeCreateView.as_view(), name='equipmenttype_add'),
    path('<int:pk>/edit/', EquipmentTypeUpdateView.as_view(), name='equipmenttype_edit'),
    path('<int:pk>/delete/', EquipmentTypeDeleteView.as_view(), name='equipmenttype_delete'),
    path('stations/', StationListView.as_view(), name='station_list'),
    path('stations/add/', StationCreateView.as_view(), name='station_add'),
    path('stations/<int:pk>/edit/', StationUpdateView.as_view(), name='station_edit'),
    path('stations/<int:pk>/delete/', StationDeleteView.as_view(), name='station_delete'),
    path('cities/add/', CityCreateView.as_view(), name='city_add'),
]
