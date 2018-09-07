from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.list import ListView
from django.http import Http404
from .forms import ComputerForm, ProcessorForm, RAMForm, DiskForm
from .models import Computer, Processor, RAM, Disk



def show_listing(request):
    forms = [
    ProcessorForm(request.GET),
    RAMForm(request.GET),
    DiskForm(request.GET),
    ]
    cpuModel = request.GET.get('cpu-model', '')
    cpuSpeed = request.GET.get('cpu-speed', '')
    ramModel = request.GET.get('ram-model', '')
    ramSpeed = request.GET.get('ram-speed', '')
    diskType = request.GET.get('disk-dtype', '')
    computers = Computer.objects.all()
    if cpuModel:
        computers = computers.filter(processor__model__icontains=cpuModel)
    if cpuSpeed:
        computers = computers.filter(processor__speed=cpuSpeed)
    if ramModel:
        computers = computers.filter(ram__model__icontains=ramModel)
    if ramSpeed:
        computers = computers.filter(ram__speed=ramSpeed)
    if diskType:
        computers = computers.filter(disk__dtype__icontains=diskType)
    return render(request, 'listing.html', {'computers': computers, 'forms': forms})

def edit(request, cid):
    computer = get_object_or_404(Computer, pk=cid)
    if request.method == 'POST':
        form = ComputerForm(request.POST, request.FILES, instance=computer)
        if form.is_valid():
            form.save()
    elif request.method == 'GET':
        form = ComputerForm(instance = computer)
    return render(request, 'edit.html', {'pc': computer, 'form': form})

def remove(request, cid):
    computer = get_object_or_404(Computer, pk = cid)
    computer.delete()
    return redirect(show_listing)

def add(request):
    if request.method == 'POST':
        form = ComputerForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect(show_listing)
    elif request.method == 'GET':
        form = ComputerForm()

    return render(request, 'add.html', {'form': form})
