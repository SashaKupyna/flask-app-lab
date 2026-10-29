import unittest
from app import app


class FlaskAppTestCase(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()

    def test_greetings_page(self):
        response = self.client.get("/users/hi/John?age=30")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"JOHN", response.data)
        self.assertIn(b"30", response.data)

    def test_admin_page(self):
        response = self.client.get("/users/admin", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"ADMINISTRATOR", response.data)
        self.assertIn(b"45", response.data)

    def test_login_page_renders(self):
        response = self.client.get("/users/login")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Login", response.data)

    def test_login_invalid_credentials(self):
        response = self.client.post(
            "/users/login",
            data={"username": "user1", "password": "wrong_password"},
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Wrong data! Try again!", response.data)

    def test_login_success_and_logout(self):
        response = self.client.post(
            "/users/login",
            data={"username": "user1", "password": "password"},
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("user1".encode("utf-8"), response.data)

        logout_response = self.client.get("/users/logout", follow_redirects=True)
        self.assertEqual(logout_response.status_code, 200)
        self.assertIn(b"Login", logout_response.data)

    def test_profile_unauthorized_redirect(self):
        response = self.client.get("/users/profile")
        self.assertEqual(response.status_code, 302)
        self.assertIn("/users/login", response.headers["Location"])

    def test_cookie_addition(self):
        self.client.post(
            "/users/login",
            data={"username": "user1", "password": "password"},
            follow_redirects=True,
        )
        response = self.client.post(
            "/users/profile/cookie/add",
            data={"key": "my_test_cookie", "value": "12345", "max_age": "3600"},
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"my_test_cookie", response.data)


if __name__ == "__main__":
    unittest.main()
