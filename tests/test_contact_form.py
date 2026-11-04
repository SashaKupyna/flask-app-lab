import unittest
import warnings
from app import app

warnings.filterwarnings("ignore", category=DeprecationWarning)


class ContactFormTestCase(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        app.config["WTF_CSRF_ENABLED"] = False
        self.client = app.test_client()

    def test_contact_page_renders(self):
        response = self.client.get("/contact")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Send Message", response.data)

    def test_contact_invalid_data(self):
        response = self.client.post(
            "/contact",
            data={
                "name": "Bob",
                "email": "invalid-email",
                "phone": "0501234567",
                "subject": "general",
                "message": "",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("Помилка валідації".encode("utf-8"), response.data)

    def test_contact_valid_data(self):
        response = self.client.post(
            "/contact",
            data={
                "name": "Sasha",
                "email": "sasha@example.com",
                "phone": "+380501234567",
                "subject": "tech",
                "message": "тестове повідомлення",
            },
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("успішно надіслано".encode("utf-8"), response.data)


if __name__ == "__main__":
    unittest.main()
