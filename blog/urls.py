
from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dash', views.dashboard, name='dash'),
    path('customer/<str:pk>', views.customer, name='customer'),
    # path('create/', views.create, name='create'),
    path('create/<str:pk>', views.create, name='create'),
    path('update/<str:pk>', views.update, name='update'),
    path('delete/<str:pk>', views.delete, name='delete'),
]
