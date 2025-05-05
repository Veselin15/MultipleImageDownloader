from django.urls import path
from . import views

urlpatterns = [
    path('', views.search_images, name='search_images'),
    path('download/', views.download_images, name='download_images'),
]