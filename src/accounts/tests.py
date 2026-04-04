from datetime import date

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import CustomerProfile


class AccountViewTests(TestCase):
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
