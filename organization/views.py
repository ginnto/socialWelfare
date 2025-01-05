from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from home.models import *


def organization_register(request):
    cat = Category.objects.all()
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

        category = get_object_or_404(Category, id=category)

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
            j_date=j_date,
        )
        organization.save()

        messages.success(request, "Organization registration successful!")
        return redirect('orglogin')
    else:
        return render(request, 'org_register.html',{'c':cat})


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
    organization = Organization.objects.get(user=request.user)  # Modify as per your model structure
    return render(request, 'orgdashboard.html', {'organization': organization})


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
        return redirect('orgaddproduct')
    categories = categ.objects.all()
    return render(request, 'orgaddproduct.html',{'categories': categories})


def orderslist(request):
    organization = get_object_or_404(Organization, id=org_id)

    # Filter the orders by the organization ID through the related products
    product_orders = ProductOrder.objects.filter(order__cart__user__org_id=organization)

    # Handle updating delivery status
    if request.method == "POST":
        product_order_id = request.POST.get("product_order_id")
        product_order = get_object_or_404(ProductOrder, id=product_order_id)
        product_order.delivery_status = not product_order.delivery_status  # Toggle the status
        product_order.save()

    return render(request, 'orgorder.html', {
        "organization": organization,
        "product_orders": product_orders,
    })



def donation(request):

    return render(request, 'orgdonation.html')

def donationreq(request):
    user = request.user
    try:
        organization = Organization.objects.get(user=user)
    except Organization.DoesNotExist:
        organization = None  # Handle if the user is not associated with an organization

    if request.method == 'POST':
        # Retrieve data from the form
        needed_amount = request.POST.get('needed_amount')
        purpose = request.POST.get('purpose')
        account_number = request.POST.get('account_number')
        ifsc_code = request.POST.get('ifsc_code')
        time_limit = request.POST.get('time_limit')


        donation_request = DonationRequest.objects.create(
            organization=organization,
            needed_amount=needed_amount,
            purpose=purpose,
            account_number=account_number,
            ifsc_code=ifsc_code,
            time_limit=time_limit,
        )

        return redirect('donation')  # Redirect to a success page after submission

    return render(request, 'orgdonationreq.html', {
        'organization': organization,
    })

@login_required
def donation_list_successful(request):
    user = request.user

    # Assuming each user can belong to one organization
    try:
        organization = user.organization  # or if you have many-to-many, you would filter here
    except Organization.DoesNotExist:
        # Handle the case where a user does not have an organization
        organization = None

    if organization:
        # Filter donations by organization and payment status (Completed)
        donations = donPayment.objects.filter(
            donation_request__organization=organization,
            payment_status='Completed'
        )
    else:
        # If no organization is found for the user, you can either show an error or leave donations empty
        donations = []

    return render(request, 'donation_list_successful.html', {'donations': donations})