from django.db import models
from home.models import *    # we call the model in the shop that is products and categorys
from django.contrib.auth.models import User   # user table

# Create your models here.

class OrderItem(models.Model):
    PENDING = 'Pending'
    COMPLETED = 'Completed'

    ORDER_STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (COMPLETED, 'Completed'),
    ]

    UNPAID = 'Unpaid'
    PAID = 'Paid'

    PAYMENT_STATUS_CHOICES = [
        (UNPAID, 'Unpaid'),
        (PAID, 'Paid'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, default=None)  # User who created the order
    prod = models.ForeignKey(products, on_delete=models.CASCADE)  # Product that is being ordered
    quan = models.IntegerField()  # Quantity of the product
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Price of the product
    active = models.BooleanField(default=True)  # Active status of the item in the cart
    order_date = models.DateTimeField(auto_now_add=True)  # Date when the order was placed
    is_ordered = models.BooleanField(default=False)  # Indicates whether this item is part of an order
    order_status = models.CharField(max_length=50,choices=ORDER_STATUS_CHOICES,default='Pending')  # Track the order status (Pending, Completed, etc.)
    payment_status = models.CharField(max_length=50,choices=PAYMENT_STATUS_CHOICES, default='Unpaid')  # Payment status (Unpaid, Paid)
    # shipping_address = models.TextField(null=True, blank=True)  # Shipping address for the order
    payment_method = models.CharField(max_length=50, null=True, blank=True)  # Payment method used
    delivery_date = models.DateTimeField(null=True, blank=True)  # Delivery date

    def total(self):
        return self.prod.price * self.quan  # Calculate the total price for this item

    def __str__(self):
        return f"{self.prod.name} - {self.quan} x {self.price}"


