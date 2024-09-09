from apps.product import models
from django.utils import timezone
import pytz
from datetime import timedelta, datetime
from django.conf import settings


class Cart:

    def __init__(self, request):

        self.session = request.session

        cart = request.session.get("cart")

        if not cart:
            cart = request.session["cart"] = {}

        self.cart = cart

        cart_expiry_str = self.session.get("cart_expiry")
        if cart_expiry_str:
            cart_expiry_naive = datetime.strptime(cart_expiry_str, "%Y-%m-%d %H:%M:%S")

            local_timezone = pytz.timezone(getattr(settings, "TIME_ZONE", "UTC"))
            cart_expiry = local_timezone.localize(cart_expiry_naive)

            if cart_expiry < timezone.now():
                self.clear_cart()

    def __iter__(self):

        for item in self.cart.values():
            product = models.Product.objects.get(id=item["ID"])
            item["total"] = item["price"] * item["quantity"]
            item["product_name"] = product.name
            item["max_quantity"] = product.quantity
            yield item

    def unique_name(self, size, color, product_id):

        result = f"{product_id}-{size}-{color}"
        return result

    def add(self, product, size="*", color="*", quantity=1):

        name = self.unique_name(size, color, product.id)

        if name not in self.cart:
            self.cart[name] = {
                "unique_name": name,
                "size": size,
                "color": color,
                "ID": product.id,
                "quantity": 0,
                "price": float(product.get_best_discounted_price()),
            }

        self.cart[name]["quantity"] += int(quantity)
        self.save()

    def remove_product(self, name):
        if name in self.cart:
            del self.cart[name]
        self.save()

    def clear_cart(self):
        self.cart.clear()
        self.session.pop("cart_expiry", None)
        self.save()

    def total_price_cart(self):
        total = 0
        for item in self.cart.values():
            total += item["price"] * item["quantity"]
        return total

    def add_subtract_quantity_product(self, name, value):
        if name in self.cart:
            self.cart[name]["quantity"] += value

        self.save()

    def save(self):
        expiry_time = timezone.now() + timedelta(minutes=30)
        self.session["cart_expiry"] = expiry_time.strftime("%Y-%m-%d %H:%M:%S")
        self.session.modified = True
