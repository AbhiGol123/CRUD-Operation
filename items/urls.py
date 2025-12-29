from django.urls import path
from . import views

urlpatterns = [
    path('', views.item_list1, name='item_list'),
    path('list/', views.item_list1, name='item_list'),
    path('new/', views.item_create1, name='item_create'),
    path('edit/<int:pk>/', views.item_update1, name='item_update'),
    path('delete/<int:pk>/', views.item_delete1, name='item_delete'),
]
