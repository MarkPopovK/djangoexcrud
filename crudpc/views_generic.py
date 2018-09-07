from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.list import ListView
from django.http import Http404
from .forms import ComputerForm, ProcessorForm, RAMForm, DiskForm
from .models import Computer, Processor, RAM, Disk


class show_listing(ListView):
    model = Computer
    template_name = 'gen/listing.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['forms'] = [
        ProcessorForm(self.request.GET),
        RAMForm(self.request.GET),
        DiskForm(self.request.GET),]
        return context


