from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('college/<int:pk>/', views.college_detail, name='college_detail'),
    path('filter/', views.filter_college, name='filter_college'),
    path('map-search/', views.map_search, name='map_search'),
    path('api/get-states/', views.get_states, name='get_states'),
    path('api/get-districts/', views.get_districts, name='get_districts'),
]
