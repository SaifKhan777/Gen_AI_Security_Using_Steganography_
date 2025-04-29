# generator/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.generate_and_stego_image, name='generate_and_stego_image'),  # This will be the entry point to the view
    path('generate/', views.generate_and_stego_image, name='generate_and_stego_image'),  # Same view for generation
]