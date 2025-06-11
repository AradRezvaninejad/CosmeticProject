from django.shortcuts import redirect
from charset_normalizer import from_bytes
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from .cart import Cart
from main.models import Product
from django.http import JsonResponse
from json import dumps
from django.conf import settings
from django.conf import settings
import requests
import json
import requests
from bs4 import BeautifulSoup

# ZP_API_REQUEST = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentRequest.json"
# ZP_API_VERIFY = (
#     f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentVerification.json"
# )
# ZP_API_STARTPAY = f"https://{sandbox}.zarinpal.com/pg/StartPay/"

# amount =   1000
# description = "پول بده من پول میخام"
# phone = "09127049185"
# CallbackURL = "http://127.0.0.1:8000/cart/verify/"

def cart_summery(request):
    cart = Cart(request)
    cart_products = []
    cart_total = cart.get_total_price()

    for product_id, item in cart.cart.items():
        try:
            product = Product.objects.get(id=product_id)
            cart_products.append(
                {
                    "product": product,
                    "quantity": item["quantity"],
                }
            )
        except Product.DoesNotExist:
            continue
    total_items = sum(item["quantity"] for item in cart.cart.values())
    return render(
        request,
        "cart/index.html",
        {
            "cart_products": cart_products,
            "total_items": total_items,
            "cart_total": cart_total,
        },
    )


def cart_add(request):
    if request.method == "POST" and request.POST.get("action") == "post":
        cart = Cart(request)
        product_id = request.POST.get("product_id")
        product = get_object_or_404(Product, id=product_id)
        cart.add(product)
        quantity = cart.cart[str(product.id)]["quantity"]
        return JsonResponse({"product_id": product_id, "quantity": quantity})
    return JsonResponse({"error": "Invalid request"}, status=400)

def cart_delete(request):
    if request.method == "POST":
        product_id = request.POST.get("product_id")
        cart = Cart(request)
        if product_id in cart.cart:
            del cart.cart[product_id]
            request.session.modified = True
    return redirect('cart')  


from django.shortcuts import redirect

def cart_update(request):
    # اگر درخواست GET بود پارامترها را از request.GET بگیر، و اگر POST بود از request.POST
    data = request.POST if request.method == "POST" else request.GET

    product_id = data.get("product_id")
    action = data.get("action")  # "increase" یا "decrease"
    
    cart = Cart(request)

    if product_id and product_id in cart.cart:
        current_qty = cart.cart[product_id]["quantity"]
        if action == "increase" and current_qty < 10:
            cart.cart[product_id]["quantity"] = current_qty + 1
        elif action == "decrease" and current_qty > 1:
            cart.cart[product_id]["quantity"] = current_qty - 1
        request.session.modified = True

    # ریدایرکت به صفحه قبلی (یا هر صفحه‌ای که می‌خوای)
    return redirect(request.META.get('HTTP_REFERER', 'index'))
