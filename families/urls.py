from django.urls import path
from . import views

app_name = 'families'

urlpatterns = [
    path('', views.family_list, name='family_list'),
    path('group/<int:pk>/', views.family_detail, name='family_detail'),
    # Add more paths as you build views
]
