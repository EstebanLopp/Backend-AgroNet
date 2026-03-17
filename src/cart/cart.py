from decimal import Decimal


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get("cart")

        if not cart:
            cart = self.session["cart"] = {}

        self.cart = cart

    def add(self, product, quantity=1, override_quantity=False):
        product_id = str(product.id)

        # Validación de disponibilidad efectiva
        if (
            not product.available
            or product.status != "published"
            or not product.store.is_active
            or product.stock <= 0
        ):
            return

        if product_id not in self.cart:
            self.cart[product_id] = {
                "quantity": 0,
                "price": str(product.price),
            }

        current_quantity = self.cart[product_id]["quantity"]

        if override_quantity:
            new_quantity = quantity
        else:
            new_quantity = current_quantity + quantity

        if new_quantity < 1:
            new_quantity = 1

        if new_quantity > product.stock:
            new_quantity = product.stock

        self.cart[product_id]["quantity"] = new_quantity
        self.save()

    def save(self):
        self.session.modified = True

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        from decimal import Decimal
        from products.models import Product

        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)

        valid_product_ids = set()
        cart = self.cart.copy()
        changed = False

        for product in products:
            product_id = str(product.id)
            valid_product_ids.add(product_id)

            if (
                not product.available
                or product.status != "published"
                or not product.store.is_active
                or product.stock <= 0
            ):
                if product_id in self.cart:
                    del self.cart[product_id]
                    changed = True
                continue
                
            if cart[product_id]["quantity"] > product.stock:
                cart[product_id]["quantity"] = product.stock
                self.cart[product_id]["quantity"] = product.stock
                changed = True

            cart[product_id]["product"] = product
            cart[product_id]["price"] = Decimal(cart[product_id]["price"])
            cart[product_id]["total_price"] = (
                cart[product_id]["price"] * cart[product_id]["quantity"]
            )

        for product_id in list(self.cart.keys()):
            if product_id not in valid_product_ids:
                del self.cart[product_id]
                changed = True

        if changed:
            self.save()

        for item in cart.values():
            if "product" in item:
                yield item

    def __len__(self):
        return sum(item["quantity"] for item in self.cart.values())

    def get_total_price(self):
        return sum(
            Decimal(item["price"]) * item["quantity"]
            for item in self.cart.values()
        )

    def clear(self):
        self.session["cart"] = {}
        self.save()