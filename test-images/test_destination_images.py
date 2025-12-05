from django.test import TestCase, override_settings
from django.core.files.uploadedfile import SimpleUploadedFile
from relecloud.models import Destination
import tempfile

@override_settings(MEDIA_ROOT=tempfile.gettempdir())
class DestinationModelTests(TestCase):

    def test_image_field_accepts_upload(self):
        image = SimpleUploadedFile("test.jpg", b"filecontent", content_type="image/jpeg")

        destination = Destination.objects.create(
            name="Test Place",
            description="Testing...",
            image=image,
        )

        # Basic checks
        self.assertIsNotNone(destination.image)
        self.assertIn("test.jpg", destination.image.name)
        self.assertTrue(destination.image.name.startswith("destinations/"))
        self.assertEqual(destination.image.size, len(b"filecontent"))

        # Cleanup created file
        destination.image.delete(save=False)
