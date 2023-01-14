from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home-page'),
    path('delete_bookmark/<str:id>', views.delete_bookmark, name='delete-bookmark'),
]
