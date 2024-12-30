from . import views
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', views.index, name='index'),  # urladdressname , function call, path name
    path('ecompage', views.ecompage, name='ecompage'),
    path('<slug:c_slug>/', views.ecompage, name='prod_cat'),
    path('search', views.searching, name='search'),
    path('<slug:c_slug>/<slug:product_slug>', views.detail, name='detail'),
]
