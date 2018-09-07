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

from django.urls import path
from . import views, views_generic


urlpatterns = [
    #path('', views.show_listing, name = 'listing'),
    #path('edit/<int:cid>', views.edit, name = 'edit'),
    #path('remove/<int:cid>', views.remove, name = 'remove'),
    #path('add/', views.add, name = 'add'),

    path('gen/', views_generic.show_listing.as_view(), name = 'listing_generic'),
    #path('gen/edit/<int:cid>', views_generic.edit, name = 'edit_generic'),
    #path('gen/remove/<int:cid>', views_generic.remove, name = 'remove_generic'),
    #path('gen/add/', views_generic.add, name = 'add_generic'),
]

