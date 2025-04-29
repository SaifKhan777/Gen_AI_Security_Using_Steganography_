from django.urls import path
from . import views

urlpatterns = [
    path('', views.decode_uploaded_image, name='decode_uploaded_image'),
    path('ajax-decode/', views.ajax_decode_image, name='ajax_decode_image'),
]