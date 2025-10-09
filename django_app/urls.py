from django.urls import path
from . import views

urlpatterns = [
    path('', views.todo_list, name='todo_list'),
    path('toggle/<int:todo_id>/', views.toggle_todo, name='toggle_todo'),
    path('delete/<int:todo_id>/', views.delete_todo, name='delete_todo'),
    path('edit/<int:todo_id>/', views.edit_todo, name='edit_todo'),
]