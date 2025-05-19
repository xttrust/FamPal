from django.urls import path
from . import views

app_name = 'families'

urlpatterns = [
    path('', views.family_list, name='family_list'),
    path('group/<int:pk>/', views.family_detail, name='family_detail'),
    path('family/<int:family_pk>/add_question/', views.add_question, name='add_question'),
    path('question/<int:question_id>/answer/', views.answer_question, name='answer_question'),
]
