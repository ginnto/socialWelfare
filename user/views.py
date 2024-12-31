from django.contrib import messages, auth
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import *

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
                return redirect('customer_dashboard')
            except Customer.DoesNotExist:
                messages.error(request, "Customer profile not found.")
                return redirect('customer_login')
        else:
            messages.error(request, "Invalid email or password.")
            return redirect('customer_login')
    else:
        return render(request, 'customer_login.html')

