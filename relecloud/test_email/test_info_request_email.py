# tests/test_info_request_email.py
from django.test import TestCase, Client, override_settings
from unittest.mock import patch
from django.urls import reverse
from django.core import mail

class InfoRequestEmailTests(TestCase):
    def setUp(self):
        self.client = Client()
        # Ajusta el nombre de la URL según vuestro proyecto
        self.url = reverse('info_request')  

    @patch('app.emails.send_info_request_email')
    def test_view_calls_send_email_and_shows_message(self, mock_send):
        """
        1) POST valid data to the info_request view
        2) assert that send_info_request_email is called
        3) assert that the response contains the success message
        """
        data = {
            'name': 'Juan',
            'email': 'juan@example.com',
            'message': 'Quiero información sobre cruceros'
        }
        response = self.client.post(self.url, data, follow=True)

        # 1. Se llama a la función de envío
        mock_send.assert_called_once()

        # 2. Se muestra mensaje al usuario (comprueba parte del mensaje de éxito)
        self.assertContains(response, "Thank you")

    @override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
    def test_send_info_request_email_sends_mail_locmem(self):
        """
        Test directo a la función send_info_request_email para comprobar
        que se coloca en outbox cuando se usa locmem backend.
        """
        # import local para evitar dependencias circulares si app.emails no existe aún
        from relecloud.emails import send_info_request_email
        send_info_request_email(
            to_email='juan@example.com',
            subject='Prueba info request',
            body='Cuerpo de prueba'
        )
        self.assertEqual(len(mail.outbox), 1)
        sent = mail.outbox[0]
        self.assertEqual(sent.to, ['juan@example.com'])
        self.assertIn('Cuerpo de prueba', sent.body)
