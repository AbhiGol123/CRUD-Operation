from django.urls import path
from . import views

urlpatterns = [
    path('', views.questionnaire_list, name='questionnaire_list'),
    path('create/', views.questionnaire_create, name='questionnaire_create'),
    path('update/<uuid:pk>/', views.questionnaire_update, name='questionnaire_update'),
    path('delete/<uuid:pk>/', views.questionnaire_delete, name='questionnaire_delete'),
]
