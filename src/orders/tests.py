from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from accounts.models import SellerProfile, Store
from products.models import Category, Product

from .models import Order, OrderItem, SellerNotification


class SellerNotificationPdfTests(TestCase):
	def setUp(self):
		self.customer = User.objects.create_user(username="cliente", password="test12345")
		self.seller_user = User.objects.create_user(username="vendedor", password="test12345")
		self.other_seller_user = User.objects.create_user(username="otro_vendedor", password="test12345")

		seller_profile = SellerProfile.objects.create(user=self.seller_user)
		other_seller_profile = SellerProfile.objects.create(user=self.other_seller_user)

		self.store = Store.objects.create(
			seller=seller_profile,
			name="Finca Central",
			description="",
			phone="3000000000",
			address="Vereda Centro",
			city="Tunja",
			is_active=True,
		)
		self.other_store = Store.objects.create(
			seller=other_seller_profile,
			name="Otra Finca",
			description="",
			phone="3111111111",
			address="Vereda Norte",
			city="Duitama",
			is_active=True,
		)

		category = Category.objects.create(name="Frutas", slug="frutas")
		self.product = Product.objects.create(
			store=self.store,
			category=category,
			name="Mango Tommy",
			description="Mango fresco",
			price="12500.00",
			stock=10,
			status="published",
			shipping_type="domicilio",
			weight_unit="kg",
			weight="1.00",
			payment_type="transferencia",
			available=True,
			image="products/test.jpg",
		)

		other_product = Product.objects.create(
			store=self.other_store,
			category=category,
			name="Papa Pastusa",
			description="Papa de cultivo local",
			price="5000.00",
			stock=10,
			status="published",
			shipping_type="domicilio",
			weight_unit="kg",
			weight="1.00",
			payment_type="transferencia",
			available=True,
			image="products/test2.jpg",
		)

		self.order = Order.objects.create(
			user=self.customer,
			paid=True,
			status="pending",
			payment_method="transfer",
			shipping_method="standard",
			address="Calle 10 # 20-30",
			city="Tunja",
			notes="Entregar en portería",
		)

		OrderItem.objects.create(
			order=self.order,
			product=self.product,
			price="12500.00",
			quantity=2,
		)
		OrderItem.objects.create(
			order=self.order,
			product=other_product,
			price="5000.00",
			quantity=1,
		)

		self.notification = SellerNotification.objects.create(store=self.store, order=self.order)

	def test_customer_can_download_order_receipt_pdf(self):
		self.client.login(username="cliente", password="test12345")

		response = self.client.get(
			reverse("orders:download_order_receipt_pdf", args=[self.order.id])
		)

		self.assertEqual(response.status_code, 200)
		self.assertEqual(response["Content-Type"], "application/pdf")
		self.assertIn("attachment; filename=", response["Content-Disposition"])
		self.assertTrue(response.content.startswith(b"%PDF"))

	def test_seller_can_download_pdf_for_own_notification(self):
		self.client.login(username="vendedor", password="test12345")

		response = self.client.get(
			reverse("orders:download_seller_notification_pdf", args=[self.notification.id])
		)

		self.assertEqual(response.status_code, 200)
		self.assertEqual(response["Content-Type"], "application/pdf")
		self.assertIn("attachment; filename=", response["Content-Disposition"])
		self.assertTrue(response.content.startswith(b"%PDF"))

	def test_seller_cannot_download_pdf_for_other_store_notification(self):
		self.client.login(username="otro_vendedor", password="test12345")

		response = self.client.get(
			reverse("orders:download_seller_notification_pdf", args=[self.notification.id])
		)

		self.assertEqual(response.status_code, 404)
