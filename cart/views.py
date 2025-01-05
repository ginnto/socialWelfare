from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseNotAllowed
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from home.models import *
from user.models import *

# Create your views here.


@login_required(login_url='Customer:login')
def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


@login_required(login_url='Customer:login')
def add_cart(request, product_id):
    user = Customer.objects.get(user_id=request.user.id)
    product = products.objects.get(id=product_id)
    try:
        cart = Cart.objects.get(user=request.user.id)
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id=_cart_id(request), user=user)
        cart.save()

    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)
        if cart_item.quantity < cart_item.product.stock:
            cart_item.quantity +=1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            product=product,
            quantity=1,
            cart=cart
        )
        cart_item.save()
    return redirect('Cart:cart_details')

@login_required(login_url='Customer:login')
def cart_details(request, total=0, counter=0, cart_items=None):
    user = request.user.id
    userid = Customer.objects.get(user_id=user)
    print('hai', userid.id)
    try:
        # Use filter to get all carts and handle if there are multiple carts
        carts = Cart.objects.filter(user=userid.id)

        if carts.exists():  # If carts exist, use the first one
            cart = carts.first()
            cart_items = CartItem.objects.filter(cart=cart, active=True)
            for cart_item in cart_items:
                total += (cart_item.product.price * cart_item.quantity)
                counter += cart_item.quantity
        else:
            cart = None  # No cart found
            cart_items = []
    except ObjectDoesNotExist:
        cart_items = []  # If cart does not exist, ensure cart_items is empty

    return render(request, 'cart/cart.html', dict(cart_items=cart_items, total=total, counter=counter))
@login_required(login_url='Customer:login')
def full_remove(request, product_id):
    cart = Cart.objects.get(user=request.user.id)
    product = get_object_or_404(products, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)
    cart_item.delete()
    return redirect('Cart:cart_details')


@login_required(login_url='Customer:login')
def cart_remove(request, product_id):
    cart = Cart.objects.get(user=request.user.id)
    product = get_object_or_404(products, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('Cart:cart_details')


@login_required(login_url='Customer:login')
def checkout(request, total=0, counter=0):
    try:
        user_details = Customer.objects.get(user_id=request.user.id)
        cart = Cart.objects.get(user_id=user_details.id)

        cart_items = CartItem.objects.filter(cart=cart, active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            counter += cart_item.quantity
        print(user_details)
    except Cart.DoesNotExist:
        print('haiiiiiiii')
        return redirect('Cart:cart_details')

    return render(request, 'cart/checkout.html', {
        'cart_items': cart_items,
        'total': total,
        'user_details': user_details,
        'cart_id': cart.id
    })

@login_required(login_url='Customer:login')
def PlaceOrder(request):
    if request.method == 'POST':
        add = request.POST['c_address']
        type = request.POST['payment_option']
        user_details = Customer.objects.get(user_id=request.user.id)
        cart = Cart.objects.get(user_id=user_details.id)
        total_amount = 0

        order = Order.objects.create(user=user_details, cart_id=cart, payment_type=type, address=add,
                                     payment_status=False)
        order.save()

        cart_item = CartItem.objects.filter(cart=cart, active=True)
        for i in cart_item:
            # Reduce stock for each product in the order
            product = i.product
            product.stock -= i.quantity
            product.save()

            total_amount += (product.price * i.quantity)

            ProductOrder.objects.create(order=order, product=product, quantity=i.quantity,
                                        product_total=product.price * i.quantity)

        order.amount = total_amount
        order.save()

        cart_item.delete()

        if type == '1':
            return render(request, 'thankyou.html')
        else:
            return redirect('Cart:payment', order.id)
    return HttpResponseNotAllowed(['POST'])



@login_required(login_url='Customer:login')
def Payments(request, order_id):
    if request.method == 'POST':
        card_number = request.POST.get('card_number')
        name = request.POST.get('card_name')
        expiry_month = request.POST.get('expiry_month')
        expiry_year = request.POST.get('expiry_year')
        cvv = request.POST.get('cvv')
        user_detail = Customer.objects.get(user_id=request.user.id)
        orders = Order.objects.get(id=order_id)

        pay = Payment(
            user=user_detail,
            order=orders,
            card_number=card_number,
            name=name,
            expiry_month=expiry_month,
            expiry_year=expiry_year,
            cvv=cvv
        )
        pay.save()

        orders.payment_status = True
        orders.save()

        return render(request, 'cart/thankyou.html')
    return render(request, 'cart/online_payment.html')


@login_required(login_url='Customer:login')
def Order_Confirmation(request):
    user = request.user.id
    userid = Customer.objects.get(user_id=user)
    cod_order = Order.objects.filter(user=userid.id)
    order_products = ProductOrder.objects.filter(order__in=cod_order).order_by('-order__date_time')

    return render(request, 'cart/order_confirmation.html', {'order_items':order_products})


