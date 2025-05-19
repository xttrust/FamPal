from django.urls import path
from . import views

urlpatterns = [
    path('', views.profile_view, name='profile'),
    path('leave-family/<int:membership_id>/', views.leave_family_view, name='leave_family'),
]
