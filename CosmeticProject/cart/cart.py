import json
from math import prod
from main.models import Product


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get("cart")
        if not cart:
            cart = self.session["cart"] = {}
        self.cart = cart

    def add(self, product):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {
                "quantity": 1,
                "price": str(product.price),
                "name": product.name,
            }
        else:
            self.cart[product_id]["quantity"] += 1
        self.session.modified = True

    def save(self,):
        self.session = json.dumps(self.cart)

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())
    
    def get_prods(self):
        product_id = self.cart.keys()
        products = Product.objects.filter(id__in=product_id)
        return products

        
    def get_total_price(self):
        return sum(
            int(item['quantity']) * float(item['price']) for item in self.cart.values()
        )
