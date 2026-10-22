import unittest
from app import app


class ProductsBlueprintTestCase(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()

    def test_products_list_page(self):
        response = self.client.get("/products/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Laptop".encode("utf-8"), response.data)
        self.assertIn("Phone".encode("utf-8"), response.data)
        self.assertIn("PC".encode("utf-8"), response.data)
        self.assertIn(b"1200", response.data)
        self.assertIn(b"800", response.data)
        self.assertIn(b"1800", response.data)

    def test_product_detail_success(self):
        response = self.client.get("/products/1")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Laptop".encode("utf-8"), response.data)
        self.assertIn("ноутбук".encode("utf-8"), response.data)
        self.assertIn(b"1200", response.data)

    def test_product_detail_not_found(self):
        response = self.client.get("/products/999")
        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()
