from django.urls import path
from . import views


app_name = 'Cart'   # for specifiy urls

urlpatterns = [
    path('', views.cart_details, name='cart_details'),
    path('add_cart/<int:product_id>/', views.add_cart, name='add_cart'),
    path('remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
    path('full_remove/<int:product_id>/', views.full_remove, name='full_remove'),
    path('checkout/', views.checkout, name='checkout'),
    path('place-order', views.PlaceOrder, name='place_order'),
    path('payment/<int:order_id>', views.Payments, name='payment'),
    path('orderview/', views.Order_Confirmation, name='orderview'),
]