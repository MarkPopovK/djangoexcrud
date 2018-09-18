from django.contrib import admin
from django.urls import path, include, reverse_lazy
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import RedirectView
from .views import Heroview



urlpatterns = [
    path('', Heroview.as_view(), name = 'heroselect'),
]