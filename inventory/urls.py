from django.shortcuts import render
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    #path('', views.index, name='index'),
    path('auth/', views.login_register, name='login_register'),
    path('home/', views.home_view, name='home'),
    path('pharmacy-info/', views.pharmacy_info, name='pharmacy_info'),
    #path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    #path('register/', views.register, name='register'),
    path('medicines/', views.manage_medicines, name='manage_medicines'),
    # path('medicines/add/', views.add_medicine, name='add_medicine'),
    # path('medicines/edit/<int:pk>/', views.edit_medicine, name='edit_medicine'),
    path('medicines/delete/<int:pk>/', views.delete_medicine, name='delete_medicine'),

    path('equipment/', views.manage_equipment, name='manage_equipment'),
    # path('equipment/add/', views.add_equipment, name='add_equipment'),
    # path('equipment/edit/<int:pk>/', views.edit_equipment, name='edit_equipment'),
    path('equipment/delete/<int:pk>/', views.delete_equipment, name='delete_equipment'),
]