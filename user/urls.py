from . import views
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('customer_register/', views.customer_register, name='customer_register'),
    path('customer_login/', views.customer_login, name='customer_login'),
    path('profile/', views.customer_profile, name='customer_profile'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('logout/', views.logout, name='logout'),
    path('donation-list/', views.donation_list_view, name='donation_list'),
    path('pay_donation/<int:id>/', views.pay_donation, name='pay_donation'),
    path('product_requests/', views.proreq_list_view, name='product_requests'),
    path('add_proreq/<int:request_id>/', views.add_proreq, name='add_proreq'),
    path('feedback/<int:product_id>/', views.feedback_form, name='feedback_form'),
    path('feedback-list/', views.user_feedback_list, name='user_feedback_list'),



]
