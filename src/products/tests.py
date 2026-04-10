from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from accounts.models import SellerProfile, Store

from .models import Category, Product


class ProductViewTests(TestCase):
	def setUp(self):
		seller_user = User.objects.create_user(username="sellerproducts", password="test12345")
		seller_profile = SellerProfile.objects.create(user=seller_user)
		self.store = Store.objects.create(
			seller=seller_profile,
			name="Finca Productos",
			description="Descripcion suficientemente larga",
			phone="3005556677",
			address="Calle 10 # 20-30",
			city="Tunja",
			is_active=True,
		)
		self.category = Category.objects.create(name="Frutas Productos", slug="frutas-productos")

	def test_product_list_only_shows_publicly_visible_products(self):
		visible_product = Product.objects.create(
			store=self.store,
			category=self.category,
			name="Banano visible",
			description="Producto visible en catalogo publico",
			price="4500.00",
			stock=5,
			status="published",
			shipping_type="domicilio",
			weight_unit="kg",
			weight="1.00",
			payment_type="transferencia",
			available=True,
			image="products/banano.jpg",
		)
		Product.objects.create(
			store=self.store,
			category=self.category,
			name="Banano oculto",
			description="Producto no visible por estado",
			price="4500.00",
			stock=5,
			status="disabled",
			shipping_type="domicilio",
			weight_unit="kg",
			weight="1.00",
			payment_type="transferencia",
			available=False,
			image="products/banano2.jpg",
		)

		response = self.client.get(reverse("products:product_list"))

		self.assertEqual(response.status_code, 200)
		page_products = list(response.context["page_obj"].object_list)
		self.assertEqual(page_products, [visible_product])

	def test_my_products_redirects_logged_user_without_store(self):
		User.objects.create_user(username="sin_tienda", password="test12345")
		self.client.login(username="sin_tienda", password="test12345")

		response = self.client.get(reverse("products:my_products"))

		self.assertEqual(response.status_code, 302)
		self.assertEqual(response.url, reverse("accounts:create_store"))

	def test_product_detail_paginates_related_products(self):
		main_product = Product.objects.create(
			store=self.store,
			category=self.category,
			name="Producto principal",
			description="Producto base del detalle publico",
			price="5000.00",
			stock=5,
			status="published",
			shipping_type="domicilio",
			weight_unit="kg",
			weight="1.00",
			payment_type="transferencia",
			available=True,
			image="products/principal.jpg",
		)

		for number in range(7):
			Product.objects.create(
				store=self.store,
				category=self.category,
				name=f"Relacionado {number}",
				description="Producto relacionado visible",
				price="4500.00",
				stock=5,
				status="published",
				shipping_type="domicilio",
				weight_unit="kg",
				weight="1.00",
				payment_type="transferencia",
				available=True,
				image=f"products/relacionado-{number}.jpg",
			)

		response = self.client.get(reverse("products:product_detail", args=[main_product.slug]))

		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.context["page_obj"].paginator.count, 7)
		self.assertEqual(len(response.context["page_obj"].object_list), 6)

		second_page_response = self.client.get(
			reverse("products:product_detail", args=[main_product.slug]),
			{"page": 2},
		)

		self.assertEqual(second_page_response.status_code, 200)
		self.assertEqual(second_page_response.context["page_obj"].number, 2)
		self.assertEqual(len(second_page_response.context["page_obj"].object_list), 1)
