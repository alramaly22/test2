from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Order, OrderItem, PromoCode
from cart.cart import Cart
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
import datetime
from decimal import Decimal
from store.models import Profile  # استيراد Profile من تطبيق store
from store.forms import UserInfoForm  # استيراد UserInfoForm من تطبيق store

@login_required
def payment_success(request):
    """
    عرض صفحة نجاح الدفع.
    """
    return render(request, 'payment/payment_success.html', {})
def checkout(request):
    cart = Cart(request)
    cart_products = cart.get_prods()
    quantities = cart.get_quants()
    totals = cart.cart_total()

    delivery_fee = Decimal('60.00')
    total_with_delivery = totals + delivery_fee

    discount_percentage = request.session.get('discount_percentage', 0)
    discount_amount = (totals * Decimal(discount_percentage)) / 100  # الخصم على totals
    final_total = totals + delivery_fee - discount_amount

    # باقي الكود...

    if request.method == 'POST':
        # إذا كان المستخدم مسجلاً دخوله نأخذ البيانات من Profile
        if request.user.is_authenticated:
            shipping_user = Profile.objects.get(user__id=request.user.id)
            shipping_form = UserInfoForm(request.POST, instance=shipping_user)
        else:
            # إذا لم يكن المستخدم مسجلاً دخوله نستخدم نموذج جديد فارغ
            shipping_form = UserInfoForm(request.POST)
        
        if shipping_form.is_valid():
            # حفظ البيانات في قاعدة البيانات
            shipping_form.save()
            messages.success(request, "Your shipping information has been updated!")
            return redirect('checkout')  # العودة لصفحة الـ checkout بعد حفظ البيانات
    else:
        # إذا كان الطلب GET نعرض النموذج المناسب
        if request.user.is_authenticated:
            shipping_user = Profile.objects.get(user__id=request.user.id)
            shipping_form = UserInfoForm(instance=shipping_user)
        else:
            shipping_form = UserInfoForm()

    return render(request, 'payment/checkout.html', {
        "cart_products": cart_products,
        "quantities": quantities,
        "totals": totals,
        "total_with_delivery": total_with_delivery,
        "delivery_fee": delivery_fee,
        "discount_amount": discount_amount,
        "final_total": final_total,
        "shipping_form": shipping_form
    })


def billing_info(request):
    if request.method == 'POST':
        my_shipping = {
            'full_name': request.POST.get('shipping_full_name'),
            'email': request.POST.get('shipping_email'),
            'address': request.POST.get('shipping_address1'),
            'city': request.POST.get('shipping_city'),
            'state': request.POST.get('shipping_state'),
            'country': request.POST.get('shipping_country'),
            'phone': request.POST.get('shipping_phone'),
        }
        request.session['my_shipping'] = my_shipping

        cart = Cart(request)
        cart_products = cart.get_prods()
        quantities = cart.get_quants()
        totals = cart.cart_total()
        delivery_fee = Decimal('60.00')
        discount_percentage = Decimal(request.session.get('discount_percentage', 0))
        discount_amount = (totals * discount_percentage) / 100  # الخصم على totals
        final_total = totals + delivery_fee - discount_amount

        return render(request, 'payment/billing_info.html', {
            "cart_products": cart_products,
            "quantities": quantities,
            "totals": totals,
            "total_with_delivery": totals + delivery_fee,
            "delivery_fee": delivery_fee,
            "final_total": final_total,
            "shipping_info": my_shipping
        })
    else:
        messages.error(request, "Access Denied.")
        return redirect('home')
def apply_promo_code(request):
    if request.method == 'POST':
        promo_code = request.POST.get('promo_code')
        promo = PromoCode.objects.filter(code=promo_code, is_active=True).first()

        if promo:
            request.session['promo_code'] = promo.code
            request.session['discount_percentage'] = float(promo.discount_percentage)

            # تأكد من أن session يتم حفظه
            request.session.modified = True

            return JsonResponse({'success': True, 'discount_percentage': promo.discount_percentage})

    return JsonResponse({'success': False})

def process_order(request):
    """
    معالجة الطلب وإنشاء سجل الطلب في قاعدة البيانات.
    """
    if request.method == 'POST':
        # استرجاع بيانات الشحن من الجلسة
        my_shipping = request.session.get('my_shipping', {})
        
        # قائمة بالحقول المطلوبة (تم إضافة 'phone' إلى القائمة)
        required_keys = ['full_name', 'email', 'address', 'city', 'state', 'country', 'phone']
        if not all(key in my_shipping for key in required_keys):
            messages.error(request, "Shipping information is incomplete or missing.")
            return redirect('checkout')
        
        # استخراج البيانات من الجلسة
        full_name = my_shipping['full_name']
        email = my_shipping['email']
        shipping_address = f"{my_shipping['address']}\n{my_shipping['city']}\n{my_shipping['state']}\n{my_shipping['country']}"
        phone = my_shipping['phone']  # استخراج رقم الهاتف

        # الحصول على بيانات العربة
        cart = Cart(request)
        cart_products = cart.get_prods()
        quantities = cart.get_quants()
        totals = cart.cart_total()

        # رسوم التوصيل ثابتة ب 60 جنيه
        delivery_fee = Decimal('60.00')
        total_with_delivery = totals + delivery_fee

        # تطبيق الخصم إذا كان هناك برومو كود
        discount_percentage = request.session.get('discount_percentage', 0)
        discount_amount = (totals * Decimal(discount_percentage)) / 100  # الخصم على totals
        amount_paid = totals + delivery_fee - discount_amount  # السعر النهائي

        # تحديد المستخدم (مسجل دخول أو غير مسجل)
        if request.user.is_authenticated:
            user = request.user
        else:
            user = None  # السماح بإنشاء الطلب بدون تسجيل دخول
        
        # إنشاء الطلب في قاعدة البيانات
        create_order = Order(
            user=user,
            full_name=full_name,
            email=email,
            shipping_address=shipping_address,
            amount_paid=amount_paid,
            phone=phone,  # إضافة رقم الهاتف
            promo_code=request.session.get('promo_code', None),  # إضافة البرومو كود
            discount_percentage=discount_percentage  # إضافة نسبة الخصم
        )
        create_order.save()

        # الحصول على معرف الطلب الذي تم إنشاؤه
        order_id = create_order.pk

        # إنشاء عناصر الطلب (Order Items)
        for product in cart_products:
            product_id = product.id
            price = product.sale_price if product.is_sale else product.price
            for key, value in quantities.items():
                if int(key) == product.id:
                    create_order_item = OrderItem(
                        order_id=order_id,
                        product_id=product_id,
                        user=user,  # يمكن أن يكون None
                        quantity=value['quantity'] if isinstance(value, dict) else value,
                        price=price,
                        size=value['size'] if isinstance(value, dict) else None
                    )
                    create_order_item.save()

        # حذف بيانات الطلب من الجلسة بعد اكتماله
        for key in list(request.session.keys()):
            if key == "session_key" or key == "promo_code" or key == "discount_percentage":
                del request.session[key]

        # إظهار رسالة نجاح
        messages.success(request, f"Order Placed! Delivery Fee: {delivery_fee} EGP. Discount: {discount_amount} EGP.")
        return redirect('home')

    else:
        # إذا لم يكن الطلب POST
        messages.error(request, "Access Denied")
        return redirect('home')
@login_required
def shipped_dash(request):
    """
    عرض لوحة التحكم للطلبات المشحونة (للمشرفين فقط).
    """
    if request.user.is_superuser:
        orders = Order.objects.filter(shipped=True)
        return render(request, 'payment/shipped_dash.html', {'orders': orders})
    else:
        messages.error(request, "Access Denied")
        return redirect('home')

@login_required
def not_shipped_dash(request):
    """
    عرض لوحة التحكم للطلبات غير المشحونة (للمشرفين فقط).
    """
    if request.user.is_superuser:
        orders = Order.objects.filter(shipped=False)
        return render(request, 'payment/not_shipped_dash.html', {'orders': orders})
    else:
        messages.error(request, "Access Denied")
        return redirect('home')

@login_required
def orders(request, pk):
    """
    عرض تفاصيل طلب معين (للمشرفين فقط).
    """
    if request.user.is_superuser:
        order = get_object_or_404(Order, id=pk)
        items = OrderItem.objects.filter(order=pk)
        return render(request, 'payment/orders.html', {'order': order, 'items': items})
    else:
        messages.error(request, "Access Denied")
        return redirect('home')