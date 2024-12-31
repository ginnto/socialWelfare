from . import views
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('organization_register',views.organization_register,name='orgregister'),
    path('organization_login',views.organization_login,name='orglogin'),
]
