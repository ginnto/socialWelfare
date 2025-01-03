from . import views
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('organization_register',views.organization_register,name='orgregister'),
    path('organization_login',views.organization_login,name='orglogin'),
    path('dashboard', views.organization_dashboard, name='orgdashboard'),
    path('orderslist', views.orderslist, name='orderslist'),
    path('donation', views.donation, name='donation'),
    path('donationreq', views.donationreq, name='donationreq'),
    path('organization_addproduct', views.organization_addproduct, name='orgaddproduct'),

]
