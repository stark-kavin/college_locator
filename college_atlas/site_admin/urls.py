from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.admin_login, name='admin_login'),
    path('logout/', views.admin_logout, name='admin_logout'),
    
    path('', views.admin_dashboard, name='admin_dashboard'),
    path('colleges/create/', views.create_college, name='create_college'),
    path('colleges/<int:pk>/edit/', views.edit_college, name='edit_college'),
    path('colleges/<int:pk>/delete/', views.delete_college, name='delete_college'),
    
    path('degrees/', views.degree_list, name='degree_list'),
    path('degrees/create/', views.create_degree, name='create_degree'),
    path('degrees/<int:pk>/edit/', views.edit_degree, name='edit_degree'),
    path('degrees/<int:pk>/delete/', views.delete_degree, name='delete_degree'),
    
    path('countries/', views.country_list, name='country_list'),
    path('countries/create/', views.create_country, name='create_country'),
    path('countries/<int:pk>/edit/', views.edit_country, name='edit_country'),
    path('countries/<int:pk>/delete/', views.delete_country, name='delete_country'),
    
    path('states/', views.state_list, name='state_list'),
    path('states/create/', views.create_state, name='create_state'),
    path('states/<int:pk>/edit/', views.edit_state, name='edit_state'),
    path('states/<int:pk>/delete/', views.delete_state, name='delete_state'),
    
    path('districts/', views.district_list, name='district_list'),
    path('districts/create/', views.create_district, name='create_district'),
    path('districts/<int:pk>/edit/', views.edit_district, name='edit_district'),
    path('districts/<int:pk>/delete/', views.delete_district, name='delete_district'),
]
