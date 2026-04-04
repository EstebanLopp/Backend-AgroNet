from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from accounts.models import SellerProfile, Store
from products.models import Category, Product


class InicioViewTests(TestCase):
	def setUp(self):
		seller_user = User.objects.create_user(username="sellerinicio", password="test12345")
		seller_profile = SellerProfile.objects.create(user=seller_user)
		self.active_store = Store.objects.create(
			seller=seller_profile,
			name="Tienda Inicio",
			description="Descripcion de tienda valida",
			phone="3001112233",
			address="Calle 1 # 2-3",
			city="Tunja",
			is_active=True,
		)

		other_user = User.objects.create_user(username="sellerinactivo", password="test12345")
		other_profile = SellerProfile.objects.create(user=other_user)
		self.inactive_store = Store.objects.create(
			seller=other_profile,
			name="Tienda Inactiva",
			description="Descripcion de tienda inactiva",
			phone="3001112244",
			address="Calle 4 # 5-6",
			city="Duitama",
			is_active=False,
		)

		self.category = Category.objects.create(name="Frutas Inicio", slug="frutas-inicio")
		Category.objects.create(name="Verduras Inicio", slug="verduras-inicio")
		Category.objects.create(name="Tuberculos Inicio", slug="tuberculos-inicio")
		Category.objects.create(name="Lacteos Inicio", slug="lacteos-inicio")
		Category.objects.create(name="Carnes Inicio", slug="carnes-inicio")

	def test_index_only_includes_visible_products_and_limits_categories(self):
		visible_product = Product.objects.create(
			store=self.active_store,
			category=self.category,
			name="Mango visible",
			description="Producto visible para el inicio",
			price="12000.00",
			stock=5,
			status="published",
			shipping_type="domicilio",
			weight_unit="kg",
			weight="1.00",
			payment_type="transferencia",
			available=True,
			image="products/mango.jpg",
		)
		Product.objects.create(
			store=self.active_store,
			category=self.category,
			name="Producto sin stock",
			description="Producto sin existencias visibles",
			price="8000.00",
			stock=0,
			status="published",
			shipping_type="domicilio",
			weight_unit="kg",
			weight="1.00",
			payment_type="transferencia",
			available=True,
			image="products/sinstock.jpg",
		)
		Product.objects.create(
			store=self.inactive_store,
			category=self.category,
			name="Producto tienda inactiva",
			description="No debe verse en el inicio",
			price="9000.00",
			stock=4,
			status="published",
			shipping_type="domicilio",
			weight_unit="kg",
			weight="1.00",
			payment_type="transferencia",
			available=True,
			image="products/inactivo.jpg",
		)

		response = self.client.get(reverse("index"))

		self.assertEqual(response.status_code, 200)
		self.assertIn(visible_product, response.context["home_products"])
		self.assertEqual(len(response.context["home_products"]), 1)
		self.assertEqual(len(response.context["home_categories"]), 4)
