from django.contrib.auth.models import User
from django.db import models


class category(models.Model):
    category = models.CharField(max_length=50)
    def __str__(self):
        return self.category

class Organization(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    orgname=models.CharField(max_length=20)
    category = models.ForeignKey(category, on_delete=models.CASCADE)
    org_city = models.CharField(max_length=50)
    org_district = models.CharField(max_length=50)
    org_pincode = models.PositiveIntegerField()
    reg_no = models.CharField(max_length=50)
    org_mail = models.EmailField()
    org_phno = models.CharField(max_length=20)
    org_poc = models.CharField(max_length=50)
    type= models.CharField(default='organization', max_length=50)
    org_poc_no = models.CharField(max_length=20)
    j_date = models.CharField(max_length=20)
    admin_approval = models.CharField(
        max_length=20,
        default='not approved',
        choices=[('approved', 'Approved'), ('not approved', 'Not Approved')]
    )

    def __str__(self):
        return self.org_name
