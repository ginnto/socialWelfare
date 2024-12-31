from datetime import datetime

from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .models import Organization
from home.models import *


def organization_register(request):
    if request.method == "POST":
        orgname = request.POST.get('orgname')  # New field to capture orgname
        category = request.POST.get('category')
        org_city = request.POST.get('org_city')
        org_district = request.POST.get('org_district')
        org_pincode = request.POST.get('org_pincode')
        reg_no = request.POST.get('reg_no')
        org_mail = request.POST.get('org_mail')
        org_phno = request.POST.get('org_phno')
        org_poc = request.POST.get('org_poc')
        org_poc_no = request.POST.get('org_poc_no')
        j_date = request.POST.get('j_date')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Validate passwords
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect("organization_register")



        if User.objects.filter(email=org_mail).exists():
            messages.error(request, "Email is already in use.")
            return redirect("orgregister")


        user = User.objects.create_user(
            username=org_mail,
            password=password,
            email=org_mail
        )
        user.save()

        organization = Organization.objects.create(
            user=user,
            orgname=orgname,  # Save the new field
            category=category,
            org_city=org_city,
            org_district=org_district,
            org_pincode=org_pincode,
            reg_no=reg_no,
            org_mail=org_mail,
            org_phno=org_phno,
            org_poc=org_poc,
            org_poc_no=org_poc_no,
            j_date=j_date,
        )
        organization.save()

        messages.success(request, "Organization registration successful!")
        return redirect('orglogin')
    else:
        return render(request, 'org_register.html')


def organization_login(request):
    if request.method == 'POST':
        org_mail = request.POST.get('org_mail')
        password = request.POST.get('password')

        user = auth.authenticate(request, username=org_mail, password=password)
        if user is not None:
            try:
                organization = Organization.objects.get(user=user)
                if organization.type == 'organization':

                    auth.login(request, user)
                    messages.success(request, "Login successful!")
                    return redirect('orgdashboard')
                else:
                    messages.error(request, "You are not authorized to log in as an organization.")
                    return redirect('orglogin')
            except Organization.DoesNotExist:
                messages.error(request, "Organization not found.")
                return redirect('orglogin')
        else:
            messages.error(request, "Invalid email or password.")
            return redirect('orglogin')
    else:
        return render(request, 'orglogin.html')

def organization_dashboard(request):
    return render(request, 'orgdashboard.html')

def organization_addproduct(request):
    if request.method == "POST":
        name = request.POST.get('name')
        desc = request.POST.get('desc')
        stock = request.POST.get('stock')
        price = request.POST.get('price')
        category = categ.objects.get(id=request.POST.get('category'))
        available = request.POST.get('available') == 'True'
        img = request.FILES.get('img')

        new_product = products(
            name=name,
            desc=desc,
            stock=stock,
            price=price,
            category=category,
            available=available,
            img=img,
            date=datetime.now(),
            org_id=request.user.organization
        )
        new_product.save()

        messages.success(request, 'Product added successfully!')
        return redirect('product_add')

    categories = categ.objects.all()

    return render(request, 'orgaddproduct.html',{'categories': categories})

