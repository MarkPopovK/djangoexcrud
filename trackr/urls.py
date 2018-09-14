from django.views.generic import RedirectView
from django.urls import path, reverse, reverse_lazy, include
from . import views

urlpatterns = [
    path('', views.trackr, name = 'trackr'),
    path('signup/', views.signup, name='authsignup'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('points/', views.PointList.as_view(), name = 'apipointslist'),
    path('points/<int:pk>/', views.PointDetail.as_view(), name = 'apipointsdetail'),
    path('api-auth/', include('rest_framework.urls')),
]
