from django.db import models

class Organization(models.Model):
    org_name = models.CharField(max_length=50)
    category = models.CharField(max_length=20)
    org_city = models.CharField(max_length=50)
    org_district = models.CharField(max_length=50)
    org_pincode = models.PositiveIntegerField()
    reg_no = models.CharField(max_length=50)
    org_mail = models.EmailField()
    org_phno = models.CharField(max_length=20)
    org_poc = models.CharField(max_length=50)
    org_poc_no = models.CharField(max_length=20)
    j_date = models.CharField(max_length=20)

    def __str__(self):
        return self.org_name
