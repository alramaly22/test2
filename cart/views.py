from django.shortcuts import render, get_object_or_404
from .cart import Cart
from store.models import Product
from django.http import JsonResponse
from django.contrib import messages
from decimal import Decimal


def cart_summary(request):
    cart = Cart(request)
    cart_products = cart.get_prods()

    totals = cart.cart_total()
    delivery_fee = Decimal('60.00')

    # حساب الخصم من الـ session
    discount_percentage = Decimal(request.session.get('discount_percentage', 0))
    discount_amount = (totals * discount_percentage) / 100
    total_after_promo = totals + delivery_fee - discount_amount

    return render(request, "cart_summary.html", {
        "cart_products": cart_products,
        "totals": totals,
        "delivery_fee": delivery_fee,
        "total_with_delivery": totals + delivery_fee,
        "promo_code": request.session.get('promo_code', None),
        "discount_percentage": discount_percentage,
        "discount_amount": discount_amount,
        "total_after_promo": total_after_promo,
    })
def cart_add(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))
        product_size = request.POST.get('product_size')  # الحصول على المقاس
        product = get_object_or_404(Product, id=product_id)
        cart.add(product=product, quantity=product_qty, size=product_size)
        cart_quantity = cart.__len__()
        response = JsonResponse({'qty': cart_quantity})
        messages.success(request, ("Product Added To Cart..."))
        return response

def cart_delete(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        cart.delete(product=product_id)
        response = JsonResponse({'product': product_id})
        messages.success(request, ("Item Deleted From Shopping Cart..."))
        return response

def cart_update(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))
        product_size = request.POST.get('product_size')  # الحصول على المقاس
        cart.update(product=product_id, quantity=product_qty, size=product_size)
        response = JsonResponse({'qty': product_qty, 'size': product_size})
        messages.success(request, ("Your Cart Has Been Updated..."))
        return response