from django.views import generic
from django.urls import reverse_lazy
from .forms import ComputerForm, ProcessorForm, RAMForm, DiskForm
from .models import Computer, Processor, RAM, Disk


class ShowListing(generic.ListView, generic.FormView):
    model = Computer
    form_class = ComputerForm
    success_url = reverse_lazy('listing')

    def get_queryset(self):
        queryset = super().get_queryset()
        cpu = self.request.GET.get('pc-processor', '')
        ram = self.request.GET.get('pc-ram', '')
        disk = self.request.GET.get('pc-disk', '')
        if cpu:
            queryset = queryset.filter(processor=cpu)
        if ram:
            queryset = queryset.filter(ram=ram)
        if disk:
            queryset = queryset.filter(disk=disk)
        return queryset


class Add(generic.CreateView):
    model = Computer
    fields = ['processor', 'ram', 'disk', 'photo']


class Edit(generic.UpdateView):
    model = Computer
    fields = ['processor', 'ram', 'disk', 'photo']


class Remove(generic.DeleteView):
    model = Computer
