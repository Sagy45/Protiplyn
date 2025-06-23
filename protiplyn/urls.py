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
from django.contrib.auth import views as auth_views
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

    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    # VehicleStorage
    path('vehicles/', VehicleStorageListView.as_view(), name='vehicle_list'),
    path('vehicles/add/', VehicleStorageCreateView.as_view(), name='vehicle_add'),
    path('vehicles/<int:pk>/edit/', VehicleStorageUpdateView.as_view(), name='vehicle_edit'),
    path('vehicles/<int:pk>/delete/', VehicleStorageDeleteView.as_view(), name='vehicle_delete'),

    # Mask
    path('masks/', MaskListView.as_view(), name='mask_list'),
    path('masks/add/', MaskCreateView.as_view(), name='mask_add'),
    path('masks/<int:pk>/edit/', MaskUpdateView.as_view(), name='mask_edit'),
    path('masks/<int:pk>/delete/', MaskDeleteView.as_view(), name='mask_delete'),

    # ADPMulti
    path('adpmulti/', ADPMultiListView.as_view(), name='adpmulti_list'),
    path('adpmulti/add/', ADPMultiCreateView.as_view(), name='adpmulti_add'),
    path('adpmulti/<int:pk>/edit/', ADPMultiUpdateView.as_view(), name='adpmulti_edit'),
    path('adpmulti/<int:pk>/delete/', ADPMultiDeleteView.as_view(), name='adpmulti_delete'),

    # ADPSingle
    path('adpsingle/', ADPSingleListView.as_view(), name='adpsingle_list'),
    path('adpsingle/add/', ADPSingleCreateView.as_view(), name='adpsingle_add'),
    path('adpsingle/<int:pk>/edit/', ADPSingleUpdateView.as_view(), name='adpsingle_edit'),
    path('adpsingle/<int:pk>/delete/', ADPSingleDeleteView.as_view(), name='adpsingle_delete'),

    # AirTank
    path('airtanks/', AirTankListView.as_view(), name='airtank_list'),
    path('airtanks/add/', AirTankCreateView.as_view(), name='airtank_add'),
    path('airtanks/<int:pk>/edit/', AirTankUpdateView.as_view(), name='airtank_edit'),
    path('airtanks/<int:pk>/delete/', AirTankDeleteView.as_view(), name='airtank_delete'),

    # PCHO
    path('pcho/', PCHOListView.as_view(), name='pcho_list'),
    path('pcho/add/', PCHOCreateView.as_view(), name='pcho_add'),
    path('pcho/<int:pk>/edit/', PCHOUpdateView.as_view(), name='pcho_edit'),
    path('pcho/<int:pk>/delete/', PCHODeleteView.as_view(), name='pcho_delete'),

    # PA
    path('pa/', PAListView.as_view(), name='pa_list'),
    path('pa/add/', PACreateView.as_view(), name='pa_add'),
    path('pa/<int:pk>/edit/', PAUpdateView.as_view(), name='pa_edit'),
    path('pa/<int:pk>/delete/', PADeleteView.as_view(), name='pa_delete'),

    # Complete
    path('completes/', CompleteListView.as_view(), name='complete_list'),
    path('completes/add/', CompleteCreateView.as_view(), name='complete_add'),
    path('completes/<int:pk>/edit/', CompleteUpdateView.as_view(), name='complete_edit'),
    path('completes/<int:pk>/delete/', CompleteDeleteView.as_view(), name='complete_delete'),

    path('stations/<int:pk>/equipment/', StationEquipmentListView.as_view(), name='station_equipment'),

    #Upcoming revision
    path('equipment/revision-upcoming/', UpcomingRevisionListView.as_view(), name='upcoming_revisions'),

    # Accounts
    path('accounts/', include('accounts.urls')),
    path('', HomeView.as_view(), name='home'),
    path('update-status-form/', views.update_status_form, name='update_status_form'),
    path("equipment/<str:model>/<int:pk>/", EquipmentDetailView.as_view(), name="equipment_detail"),


]
