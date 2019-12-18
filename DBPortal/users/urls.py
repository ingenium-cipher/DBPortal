from django.urls import path
from . import views

urlpatterns = [
    path('register_staff/', views.register_staff, name='register_staff'),
    path('register_dber/', views.register_dber, name='register_dber'),
    path('', views.home, name='home'),
    path('ajax/load-cities/', views.load_cities, name='ajax_load_cities'),
]
