from django.contrib.auth.models import User
from django.db import models

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    type = models.CharField(default='user', max_length=50)
    photo = models.ImageField(upload_to='userimage')
    cust_name = models.CharField(max_length=50)
    cust_gender = models.CharField(max_length=20)
    cust_houseno = models.CharField(max_length=50)
    cust_city = models.CharField(max_length=50)
    cust_district = models.CharField(max_length=50)
    cust_pincode = models.IntegerField()
    cust_email = models.EmailField(max_length=50)
    cust_phno = models.CharField(max_length=50)

    def __str__(self):
        return self.cust_name

