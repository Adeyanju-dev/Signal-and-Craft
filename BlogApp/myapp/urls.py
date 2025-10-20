from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('post/new/', views.post_create, name='post-create'),
    path('post/detail/<int:pk>/', views.post_detail, name='post-detail'),
    path('post/edit/<int:pk>/', views.post_edit, name='post-edit'),
    path('post/delete/<int:pk>', views.post_delete, name='post-delete'),
]