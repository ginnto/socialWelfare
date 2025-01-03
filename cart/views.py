from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from home.models import *
from django.db.models import F
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required

# Create your views here.
def c_id(request):
    ct_id = request.session.session_key  # if session key is exist
    if not ct_id:
        ct_id = request.session.create()  # there is no session key,then create new one
    return ct_id



@login_required(login_url='login')
def add_cart(request, product_id):

    prod = products.objects.get(id=product_id)
    user = request.user

    try:
        ct=OrderItem.objects.get(user=user)    #already existing
        c_items = OrderItem.objects.get(prod=prod, cart=ct)  # same product existing
        if c_items.quan < c_items.prod.stock:
            c_items.quan += 1  # quan = quan + 1
            prod.stock -= 1
            prod.save()
        c_items.save()
    except OrderItem.DoesNotExist:                                 #cartlist
        ct=OrderItem.objects.create(user=user,prod=prod,quan=1,price=100)    #new user          #c/n
        ct.save()




    return redirect('cartDetails')  # Redirect to the cart details page



@login_required(login_url='login')
def cart_details(request):
    user = request.user
    order_items = OrderItem.objects.filter(user=user, is_ordered=False, active=True)

    # Calculate the total price of the cart
    total_price = sum(item.total() for item in order_items)

    return render(request, 'cart.html', {'order_items': order_items, 'total_price': total_price})


@login_required(login_url='login')
def min_cart(request, product_id):
    user = request.user
    order_item = get_object_or_404(OrderItem, user=user, prod__id=product_id, is_ordered=False, active=True)

    if order_item.quan > 1:
        order_item.quan -= 1
        order_item.save()
    else:
        order_item.delete()  # If the quantity is 1, delete the item from the cart

    return redirect('cart_details')


@login_required(login_url='login')
def cart_delete(request, product_id):
    user = request.user
    order_item = get_object_or_404(OrderItem, user=user, prod__id=product_id, is_ordered=False, active=True)
    order_item.delete()  # Delete the item from the cart

    return redirect('cart_details')


#
# def checkout(request):
#     if request.method == 'POST':
#         firstname = request.POST['fname']
#         lastname = request.POST['lname']
#         country = request.POST['country']
#         address = request.POST['address']
#         towncity = request.POST['city']
#         postcodezip = request.POST['pin']
#         phone = request.POST['phone']
#         email = request.POST['email']
#         cart = cartlist.objects.filter(user=request.user).first()
#
#         check = Checkout(
#             user=request.user,
#             cart=cart,
#             firstname=firstname,
#             lastname=lastname,
#             country=country,
#             address=address,
#             towncity=towncity,
#             postcodezip=postcodezip,
#             phone=phone,
#             email=email
#         )
#         check.save()
#         return redirect('payment')
#     return render(request, 'checkout.html')
#
#
# def payments(request):
#     if request.method == 'POST':
#         account_number = request.POST.get('account_number')
#         name = request.POST.get('name')
#         expiry_month = request.POST.get('expiry_month')
#         expiry_year = request.POST.get('expiry_year')
#         cvv = request.POST.get('cvv')
#
#         pay = payment(
#             user=request.user,
#             account_number=account_number,
#             name=name,
#             expiry_month=expiry_month,
#             expiry_year=expiry_year,
#             cvv=cvv
#         )
#         pay.save()
#
#         user = request.user
#         ct = cartlist.objects.get(user=user)
#         items.objects.filter(cart=ct).delete()
#
#         return render(request, 'successful.html')
#
#     return render(request, 'bank.html')
#
#
# # def success(request):
#
# #     return render(request,'successful.html')
#
# def orders(request):
#
#      return render(request,'orders.html')
#
