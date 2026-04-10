from datetime import date

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import CustomerProfile, SellerProfile, Store
from products.models import Category, Product


class AccountViewTests(TestCase):
	def setUp(self):
		self.category = Category.objects.create(name="Frutas cuentas", slug="frutas-cuentas")

	def test_create_store_redirects_when_profile_lacks_document_data(self):
		user = User.objects.create_user(username="cliente_store", password="test12345")
		self.client.login(username="cliente_store", password="test12345")

		response = self.client.get(reverse("accounts:create_store"))

		self.assertRedirects(response, reverse("accounts:edit_profile"))

	def test_delete_account_anonymizes_customer_data(self):
		user = User.objects.create_user(
			username="cliente_borrar",
			password="test12345",
			email="cliente@demo.com",
			first_name="Cliente",
			last_name="Demo",
		)
		profile = user.customer_profile
		profile.phone = "3001234567"
		profile.document_type = "cc"
		profile.document_number = "12345678"
		profile.birth_date = date(1990, 1, 1)
		profile.address = "Calle 1 # 2-3"
		profile.city = "Tunja"
		profile.save()
		seller_profile = SellerProfile.objects.create(user=user)
		store = Store.objects.create(
			seller=seller_profile,
			name="Tienda del cliente",
			description="Descripcion valida de la tienda",
			phone="3001234567",
			address="Calle 1 # 2-3",
			city="Tunja",
			is_active=True,
		)
		self.client.login(username="cliente_borrar", password="test12345")

		response = self.client.post(reverse("accounts:delete_account"))

		self.assertRedirects(response, reverse("index"))
		user.refresh_from_db()
		profile = CustomerProfile.objects.get(user=user)

		self.assertFalse(user.is_active)
		self.assertTrue(user.username.startswith("deleted_user_"))
		self.assertEqual(user.first_name, "")
		self.assertEqual(user.last_name, "")
		self.assertEqual(profile.phone, "")
		self.assertEqual(profile.document_number, "")
		self.assertEqual(profile.address, "")
		self.assertFalse(Store.objects.filter(pk=store.pk).exists())
		self.assertFalse(SellerProfile.objects.filter(pk=seller_profile.pk).exists())

	def test_public_store_detail_paginates_products(self):
		seller_user = User.objects.create_user(username="seller_publico", password="test12345")
		seller_profile = SellerProfile.objects.create(user=seller_user)
		store = Store.objects.create(
			seller=seller_profile,
			name="Tienda publica",
			description="Descripcion valida de la tienda publica",
			phone="3009876543",
			address="Calle 4 # 5-6",
			city="Tunja",
			is_active=True,
		)

		for number in range(7):
			Product.objects.create(
				store=store,
				category=self.category,
				name=f"Producto tienda {number}",
				description="Producto visible en tienda publica",
				price="4800.00",
				stock=5,
				status="published",
				shipping_type="domicilio",
				weight_unit="kg",
				weight="1.00",
				payment_type="transferencia",
				available=True,
				image=f"products/tienda-{number}.jpg",
			)

		response = self.client.get(reverse("accounts:public_store_detail", args=[store.pk]))

		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.context["page_obj"].paginator.count, 7)
		self.assertEqual(len(response.context["page_obj"].object_list), 6)

		second_page_response = self.client.get(
			reverse("accounts:public_store_detail", args=[store.pk]),
			{"page": 2},
		)

		self.assertEqual(second_page_response.status_code, 200)
		self.assertEqual(second_page_response.context["page_obj"].number, 2)
		self.assertEqual(len(second_page_response.context["page_obj"].object_list), 1)
