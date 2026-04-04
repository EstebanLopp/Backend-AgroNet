from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from accounts.models import SellerProfile, Store
from products.models import Category, Product


class CartViewTests(TestCase):
	def setUp(self):
		seller_user = User.objects.create_user(username="sellercart", password="test12345")
		seller_profile = SellerProfile.objects.create(user=seller_user)
		store = Store.objects.create(
			seller=seller_profile,
			name="Tienda Carrito",
			description="Descripcion valida de tienda",
			phone="3002223344",
			address="Calle 8 # 9-10",
			city="Tunja",
			is_active=True,
		)
		category = Category.objects.create(name="Categoria Carrito", slug="categoria-carrito")
		self.product = Product.objects.create(
			store=store,
			category=category,
			name="Tomate chonto",
			description="Tomate fresco para pruebas de carrito",
			price="3200.00",
			stock=3,
			status="published",
			shipping_type="domicilio",
			weight_unit="kg",
			weight="1.00",
			payment_type="transferencia",
			available=True,
			image="products/tomate.jpg",
		)

	def test_cart_add_creates_session_entry(self):
		response = self.client.post(reverse("cart:cart_add", args=[self.product.id]))

		self.assertRedirects(response, reverse("cart:cart_detail"))
		cart = self.client.session.get("cart", {})
		self.assertIn(str(self.product.id), cart)
		self.assertEqual(cart[str(self.product.id)]["quantity"], 1)

	def test_cart_update_clamps_quantity_to_available_stock(self):
		self.client.post(reverse("cart:cart_add", args=[self.product.id]))

		response = self.client.post(
			reverse("cart:cart_update", args=[self.product.id]),
			{"quantity": 99},
		)

		self.assertRedirects(response, reverse("cart:cart_detail"))
		cart = self.client.session.get("cart", {})
		self.assertEqual(cart[str(self.product.id)]["quantity"], 3)
