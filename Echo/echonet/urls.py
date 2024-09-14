from django.urls import path
from . import views

urlpatterns = [
    path('', views.echo_list, name='echo_list'),
    path('create/', views.echo_create, name='echo_create'),

    path('<int:echo_id>/edit/', views.echo_edit, name='echo_edit'),
    path('<int:echo_id>/delete/', views.echo_delete, name='echo_delete'),
    path('register/', views.register, name='register'),

] 
