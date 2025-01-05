from django.contrib.auth.models import User
from django.db import models


class Category(models.Model):
    category = models.CharField(max_length=50)
    def __str__(self):
        return self.category

class Organization(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    orgname=models.CharField(max_length=20)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    org_city = models.CharField(max_length=50)
    org_district = models.CharField(max_length=50)
    org_pincode = models.PositiveIntegerField()
    reg_no = models.CharField(max_length=50)
    org_mail = models.EmailField()
    org_phno = models.CharField(max_length=20)
    org_poc = models.CharField(max_length=50)
    type= models.CharField(default='organization', max_length=50)
    j_date = models.CharField(max_length=20)
    admin_approval = models.CharField(
        max_length=20,
        default='not approved',
        choices=[('approved', 'Approved'), ('not approved', 'Not Approved')]
    )

    def __str__(self):
        return self.orgname

class DonationRequest(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='donation_requests')  # Link to the organization
    needed_amount = models.DecimalField(max_digits=10, decimal_places=2)  # Amount needed to reach the goal
    purpose = models.TextField()  # Purpose of the donation
    account_number = models.CharField(max_length=20)  # Bank account number for donations
    ifsc_code = models.CharField(max_length=11)  # IFSC code for the bank account
    time_limit = models.DateField()  # Deadline for the donation goal

    def __str__(self):
        return f"Donation Request: {self.goal_name} by {self.organization.name}"


class donPayment(models.Model):
    PENDING = 'Pending'
    COMPLETED = 'Completed'
    FAILED = 'Failed'

    PAYMENT_STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (COMPLETED, 'Completed'),
        (FAILED, 'Failedn '),
    ]

    donation_request = models.ForeignKey(DonationRequest, on_delete=models.CASCADE)  # Link to the donation request
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # User who made the payment
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Amount paid
    payment_method = models.CharField(max_length=50)  # Payment method used (e.g., PayPal, Credit Card)
    payment_status = models.CharField(max_length=50, choices=PAYMENT_STATUS_CHOICES, default=PENDING)  # Payment status
    transaction_id = models.CharField(max_length=100, null=True, blank=True)  # Transaction ID for record-keeping
    payment_date = models.DateTimeField(auto_now_add=True)  # Payment date

    def __str__(self):
        return f"Payment for {self.donation_request.goal_name} by {self.user.username} - {self.payment_status}"
