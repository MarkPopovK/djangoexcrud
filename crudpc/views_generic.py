from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.http import Http404
from .forms import ComputerForm, ProcessorForm, RAMForm, DiskForm
from .models import Computer, Processor, RAM, Disk


class ShowListing(generic.ListView):
    model = Computer

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['forms'] = [
        #     ProcessorForm(self.request.GET),
        #     RAMForm(self.request.GET),
        #     DiskForm(self.request.GET),]
        return context


class Add(generic.CreateView):
    model = Computer
    fields = ['processor', 'ram', 'disk', 'photo']


class Edit(generic.UpdateView):
    model = Computer
    fields = ['processor', 'ram', 'disk', 'photo']


class Remove(generic.DeleteView):
    model = Computer



