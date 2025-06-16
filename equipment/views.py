from django.shortcuts import render
from .models import EquipmentType
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

class EquipmentTypeListView(ListView):
    model = EquipmentType
    template_name = 'equipment/equipmenttype_list.html'
    context_object_name = 'equipment_types'


class EquipmentTypeCreateView(CreateView):
    model = EquipmentType
    fields = ['name']
    template_name = 'equipment/equipmenttype_form.html'
    success_url = reverse_lazy('equipmenttype_list')


class EquipmentTypeUpdateView(UpdateView):
    model = EquipmentType
    fields = ['name']
    template_name = 'equipment/equipmenttype_form.html'
    success_url = reverse_lazy('equipmenttype_list')


class EquipmentTypeDeleteView(DeleteView):
    model = EquipmentType
    template_name = 'equipment/equipmenttype_confirm_delete.html'
    success_url = reverse_lazy('equipmenttype_list')
