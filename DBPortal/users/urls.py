from django.urls import path
from . import views

urlpatterns = [
    # path('register_staff/', views.register_staff, name='register_staff'),
    path('register_dber/', views.register_dber, name='register_dber'),
    path('', views.home, name='home'),
    path('ajax/load-cities/', views.load_cities, name='ajax_load_cities'),
    path('staff_login/', views.staff_login, name='staff_login'),
    path('dber_login/', views.dber_login, name='dber_login'),
    path('logout/', views.user_logout, name='logout'),
    path('link_dber/', views.link_dber, name='link_dber'),
    path('change_password/', views.change_password, name='change_password'),
]
