"""pcmonitor URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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

from django.urls import path, reverse, reverse_lazy
from . import views, views_generic
from .models import *

urlpatterns = [
    # path('', views.show_listing, name = 'listing'),
    # path('edit/<int:cid>', views.edit, name = 'edit'),
    # path('remove/<int:cid>', views.remove, name = 'remove'),
    # path('add/', views.add, name = 'add'),
    path('gen/', views_generic.ShowListing.as_view(model=Computer), name='listing'),

    path('gen/edit/<int:pk>', views_generic.Edit.as_view(
        model=Computer,
        success_url=reverse_lazy('listing')), name='edit'),

    path('gen/remove/<int:pk>', views_generic.Remove.as_view(
        model=Computer,
        success_url=reverse_lazy('listing')), name='remove'),

    path('gen/add/', views_generic.Add.as_view(
        model=Computer,
        success_url=reverse_lazy('listing')), name='add'),
]
