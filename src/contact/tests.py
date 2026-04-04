from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse

from .models import ContactMessage


class ContactViewTests(TestCase):
	@patch("contact.views.send_templated_email")
	def test_valid_contact_post_creates_message_and_redirects(self, mock_send_email):
		response = self.client.post(
			reverse("contact:contact"),
			{
				"nombre": "Carlos Perez",
				"identificacion": "12345678",
				"correo": "CARLOS@EXAMPLE.COM",
				"telefono": "+57 3001234567",
				"solicitud": "informacion",
				"contacto": "correo",
				"asunto": "Necesito ayuda",
				"mensaje": "Quiero recibir información sobre los pedidos.",
				"honeypot": "",
			},
		)

		self.assertRedirects(response, reverse("contact:contact_success"))
		self.assertEqual(ContactMessage.objects.count(), 1)
		message = ContactMessage.objects.get()
		self.assertEqual(message.correo, "carlos@example.com")
		mock_send_email.assert_called_once()
