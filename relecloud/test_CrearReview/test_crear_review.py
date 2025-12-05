# relecloud/test_CrearReview/test_crear_review.py

from django.test import TestCase, Client
from django.contrib.auth import get_user_model
# from django.urls import reverse   # lo usaremos más adelante cuando exista la URL
from django.core.exceptions import ObjectDoesNotExist

from relecloud.models import Destination, Cruise

try:
    from relecloud.models import Review
    REVIEW_MODEL_EXISTS = True
except ImportError:
    Review = None
    REVIEW_MODEL_EXISTS = False

User = get_user_model()


class CrearReviewTests(TestCase):
    """
    Tests TDD para el PBI PT3 (Reviews)

    Casos mínimos (según la tarea T1):
    1. Usuario CON compra -> puede crear review exitosamente
    2. Usuario SIN compra -> no puede crear review (acceso denegado)
    """

    def setUp(self):
        self.client = Client()

        self.user_with_purchase = User.objects.create_user(
            username="buyer",
            email="buyer@example.com",
            password="testpass123"
        )

        self.user_without_purchase = User.objects.create_user(
            username="nobuyer",
            email="nobuyer@example.com",
            password="testpass123"
        )

        self.destination = Destination.objects.create(
            name="Barcelona Beach Resort",
            description="Hermoso destino en la costa de Barcelona"
        )

        self.cruise = Cruise.objects.create(
            name="Mediterranean Cruise 2025",
            description="Crucero de lujo por el Mediterráneo"
        )

    def test_usuario_con_compra_crea_review_exitosamente(self):
        """
        T1-01: Usuario autenticado CON compra puede crear una review.
        """
        login_success = self.client.login(
            username="buyer",
            password="testpass123"
        )
        self.assertTrue(login_success, "Usuario comprador no pudo autenticarse")

        # TODO (T3): cambiar este path por reverse('destination_review_create', args=[self.destination.id])
        url = f"/destinations/{self.destination.id}/reviews/create/"

        review_data = {
            "rating": 5,
            "comment": "Excelente destino, muy recomendado para familias",
            "title": "Una experiencia memorable",
        }

        response = self.client.post(url, review_data, follow=True)

        self.assertIn(
            response.status_code,
            [200, 201, 302],
            f"Status code inesperado: {response.status_code}. Response: {response.content[:200]}"
        )

        self.assertTrue(
            REVIEW_MODEL_EXISTS,
            "El modelo Review debe existir"
        )

        self.assertEqual(
            Review.objects.count(),
            1,
            "Debe crearse exactamente una review"
        )

        created_review = Review.objects.first()
        self.assertEqual(created_review.user, self.user_with_purchase)
        self.assertEqual(created_review.destination, self.destination)
        self.assertEqual(created_review.rating, 5)
        self.assertEqual(
            created_review.comment,
            "Excelente destino, muy recomendado para familias"
        )
        self.assertEqual(
            created_review.title,
            "Una experiencia memorable"
        )

    def test_usuario_sin_compra_no_puede_crear_review(self):
        """
        T1-02: Usuario autenticado SIN compra recibe error al intentar crear review.
        """
        login_success = self.client.login(
            username="nobuyer",
            password="testpass123"
        )
        self.assertTrue(login_success, "Usuario sin compra no pudo autenticarse")

        # TODO (T3): cambiar este path por reverse('destination_review_create', args=[self.destination.id])
        url = f"/destinations/{self.destination.id}/reviews/create/"

        review_data = {
            "rating": 3,
            "comment": "Intento de review sin compra",
            "title": "Sin autorización",
        }

        response = self.client.post(url, review_data, follow=True)

        self.assertIn(
            response.status_code,
            [302, 403],
            f"Debería rechazar acceso. Status code: {response.status_code}"
        )

        if REVIEW_MODEL_EXISTS:
            review_count = Review.objects.count()
            self.assertEqual(
                review_count,
                0,
                f"No debe crearse review para usuario sin compra. Encontradas: {review_count}"
            )
