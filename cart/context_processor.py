from . views import *
from home.views import *

def cate(request):
    cat=categ.objects.all()
    return {'ct':cat}


def cart_total(request):
    total_price = 0
    item_count = 0

    if request.user.is_authenticated:
        user = request.user
        order_items = OrderItem.objects.filter(user=user, is_ordered=False, active=True)

        # Calculate total price and item count for the cart
        for item in order_items:
            total_price += item.total()
            item_count += item.quan

    return {'cart_total_price': total_price, 'cart_item_count': item_count}