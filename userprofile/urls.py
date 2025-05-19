from django.urls import path
from . import views

urlpatterns = [
    path('', views.profile_view, name='profile'),
    path('create-family/', views.create_family_group, name='create_family'),
    path('add-family-member/', views.add_family_member, name='add_family_member'),
    path('remove-member/<str:username>/', views.remove_family_member, name='remove_family_member'),
    path('delete-family/<int:group_id>/', views.delete_family_group, name='delete_family'),
    path('leave-family/<int:membership_id>/', views.leave_family_view, name='leave_family'),
]
