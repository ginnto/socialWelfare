from . import views
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('customer_register/', views.customer_register, name='customer_register'),
    path('customer_login/', views.customer_login, name='customer_login'),

]
