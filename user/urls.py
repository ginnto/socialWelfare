from . import views
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('customer_register/', views.customer_register, name='customer_register'),
    path('customer_login/', views.customer_login, name='customer_login'),
    path('profile/', views.customer_profile, name='customer_profile'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('logout/', views.logout, name='logout'),

]
