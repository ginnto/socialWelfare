from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import CustomerProfileForm
from .models import *
from organization.models import *

def customer_register(request):
    if request.method == "POST":
        cust_name = request.POST.get('cust_name')
        cust_gender = request.POST.get('cust_gender')
        cust_houseno = request.POST.get('cust_houseno')
        cust_city = request.POST.get('cust_city')
        cust_district = request.POST.get('cust_district')
        cust_pincode = request.POST.get('cust_pincode')
        cust_email = request.POST.get('cust_email')
        cust_phno = request.POST.get('cust_phno')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        photo = request.FILES.get('photo')

        # Validate passwords
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect("customer_register")

        # Check if the email already exists
        if User.objects.filter(email=cust_email).exists():
            messages.error(request, "Email is already in use.")
            return redirect("customer_register")

        # Create user
        user = User.objects.create_user(
            username=cust_email,
            password=password,
            email=cust_email
        )
        user.save()

        # Create customer profile
        customer = Customer.objects.create(
            user=user,
            cust_name=cust_name,
            cust_gender=cust_gender,
            cust_houseno=cust_houseno,
            cust_city=cust_city,
            cust_district=cust_district,
            cust_pincode=cust_pincode,
            cust_email=cust_email,
            cust_phno=cust_phno,
            photo=photo
        )
        customer.save()

        messages.success(request, "Customer registration successful!")
        return redirect('customer_login')
    else:
        return render(request, 'customer_register.html')

def customer_login(request):
    if request.method == 'POST':
        cust_email = request.POST.get('cust_email')
        password = request.POST.get('password')

        user = auth.authenticate(request, username=cust_email, password=password)
        if user is not None:
            try:
                customer = Customer.objects.get(user=user)
                auth.login(request, user)
                messages.success(request, "Login successful!")
                return redirect('ecompage')
            except Customer.DoesNotExist:
                messages.error(request, "Customer profile not found.This login only for Customers  ")
                return redirect('customer_login')
        else:
            messages.error(request, "Invalid email or password.")
            return redirect('customer_login')
    else:
        return render(request, 'customer_login.html')

def customer_profile(request):
    customer = Customer.objects.get(user=request.user)
    return render(request, 'customer_profile.html', {'customer': customer})


@login_required
def edit_profile(request):
    customer = Customer.objects.get(user=request.user)
    if request.method == 'POST':
        form = CustomerProfileForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('customer_profile')
    else:
        form = CustomerProfileForm(instance=customer)
    return render(request, 'edit_profile.html', {'form': form})


def donation_list_view(request):
    donation_requests = DonationRequest.objects.all()

    return render(request, 'donation_list.html', {
        'donation_requests': donation_requests
    })

@login_required
def pay_donation(request, id):
    # Fetch the donation request
    donation_request = DonationRequest.objects.get(id=id)

    if request.method == "POST":

        amount = donation_request.needed_amount  # Payment amount is the needed amount for the donation request
        payment_method = request.POST['payment_method']
        payment = donPayment.objects.create(
            donation_request=donation_request,
            user=request.user,
            amount=amount,
            payment_method=payment_method,
            payment_status=donPayment.COMPLETED,  # Assuming payment was successful
            transaction_id="dummy_transaction_id_123"  # This would be from your payment gateway
        )
        payment.save()

        # Redirect to a success page or a thank you page
        return redirect('customer_profile')

    return render(request, 'pay_donation.html', {
        'donation_request': donation_request
    })


def logout(request):
    auth.logout(request)
    return redirect('/')