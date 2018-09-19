from django.shortcuts import render, redirect
from django.utils import timezone
from .serializers import PointSerializer
from rest_framework import generics as rest_generics
from .models import TrackPoint
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
import time

# Create your views here.
@login_required(login_url=reverse_lazy('login'))
def trackr(request):
    t = time.time()
    sdict = {
        True: 'Start',
        False: 'Stop',
        'Start': True,
        'Stop': False}
    if request.method == 'POST':
        lastpoint = TrackPoint.objects.all().filter(owner=request.user).filter(date__gte=timezone.now().date()). \
            order_by('-date').first()
        start = sdict[request.POST['start']]
        if not lastpoint or not (lastpoint.start == start):
            TrackPoint.objects.create(owner=request.user, start=start)

    lastpoint = TrackPoint.objects.all().filter(owner=request.user).filter(date__gte=timezone.now().date()).\
        order_by('-date').first()
    data = {}


    if lastpoint:
        data['lastpoint'] = lastpoint
        data['start'] = not lastpoint.start
        elapsed, rested, segments, elapsedseconds = lastpoint.get_total_time()
        data['elapsed'] = elapsed
        data['rested'] = rested
        data['segments'] = segments
        data['elapsedsec'] = elapsedseconds
    else:
        data['lastpoint'] = 'no points yet'
        data['start'] = True
        data['elapsed'] = 'no time worked'
    print(time.time()-t, 'sec')
    return render(request, 'home.html', data)


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('trackr')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})







### REST API

class PointList(rest_generics.ListCreateAPIView):
    queryset = TrackPoint.objects.all()
    serializer_class = PointSerializer
    def perform_create(self, serializer):
        serializer.save(date=timezone.now())

class PointDetail(rest_generics.RetrieveUpdateDestroyAPIView):
    queryset = TrackPoint.objects.all()
    serializer_class = PointSerializer