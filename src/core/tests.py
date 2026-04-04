from django.core import mail
from django.test import TestCase, override_settings

from core.services.email_service import send_templated_email


@override_settings(
	EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
	DEFAULT_FROM_EMAIL="noreply@agronet.test",
)
class EmailServiceTests(TestCase):
	def test_send_templated_email_delivers_html_message(self):
		send_templated_email(
			subject="Confirmacion AgroNet",
			to=["cliente@example.com"],
			template_html="emails/contact_received.html",
			context={
				"nombre": "Cliente Demo",
				"asunto": "Consulta",
				"mensaje": "Necesito información sobre mi pedido.",
				"solicitud_label": "Consultas sobre productos",
			},
		)

		self.assertEqual(len(mail.outbox), 1)
		message = mail.outbox[0]
		self.assertEqual(message.subject, "Confirmacion AgroNet")
		self.assertEqual(message.to, ["cliente@example.com"])
		self.assertEqual(message.from_email, "noreply@agronet.test")
		self.assertEqual(len(message.alternatives), 1)
		self.assertEqual(message.alternatives[0][1], "text/html")
		self.assertIn("Cliente Demo", message.alternatives[0][0])
