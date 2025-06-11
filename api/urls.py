from django.contrib import admin
from django.urls import path,include
from . import views
from django.conf import settings
from django.urls import path
from .views import BlogCreateAPIView ,BlogDetailAPIView

urlpatterns = [
    path('Blog/', BlogCreateAPIView.as_view(), name='create_blog'),
    path('Blog/<str:slug>/', BlogDetailAPIView.as_view(), name='blog-detail'),
    
]