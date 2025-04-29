from django.urls import path
from . import views

urlpatterns = [
    path('encode/', views.encode_image_view, name='encode_image'),
    path('decode/', views.decode_image_view, name='decode_image'),
]