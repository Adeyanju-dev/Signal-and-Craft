from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("post/new/", views.post_create, name="post-create"),
    path("post/<slug:slug>/", views.post_detail, name="post-detail"),
    path("post/<slug:slug>/edit/", views.post_edit, name="post-edit"),
    path("post/<slug:slug>/delete/", views.post_delete, name="post-delete"),
]
