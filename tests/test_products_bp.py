import unittest
from app import app
from app.products.db import init_db


class ProductsBlueprintTestCase(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        app.config["WTF_CSRF_ENABLED"] = False
        self.client = app.test_client()
        init_db()

    def test_products_list_page(self):
        response = self.client.get("/products/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Laptop".encode("utf-8"), response.data)
        self.assertIn("Phone".encode("utf-8"), response.data)
        self.assertIn("PC".encode("utf-8"), response.data)

    def test_product_detail_success(self):
        response = self.client.get("/products/1")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Laptop".encode("utf-8"), response.data)
        self.assertIn("ноутбук".encode("utf-8"), response.data)

    def test_product_detail_not_found(self):
        response = self.client.get("/products/999")
        self.assertEqual(response.status_code, 404)

    def test_product_create_success(self):
        response = self.client.post(
            "/products/add",
            data={
                "name": "Tablet Pro",
                "category": "Планшети",
                "price": "650.00",
                "quantity": 7,
                "content": "Сучасний швидкий планшет для малювання та ігор.",
            },
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("Tablet Pro".encode("utf-8"), response.data)
        self.assertIn("успішно додано".encode("utf-8"), response.data)

    def test_product_edit_success(self):
        response = self.client.post(
            "/products/1/edit",
            data={
                "name": "Laptop Ultra",
                "category": "Комп'ютери",
                "price": "1350.00",
                "quantity": 4,
                "content": "Оновлений ноутбук з покращеним екраном.",
            },
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("Laptop Ultra".encode("utf-8"), response.data)
        self.assertIn("успішно оновлено".encode("utf-8"), response.data)

    def test_product_delete_success(self):
        # Create a temp product to delete
        self.client.post(
            "/products/add",
            data={
                "name": "Товар для видалення",
                "category": "Аксесуари",
                "price": "50.00",
                "quantity": 1,
                "content": "Тестовий опис товару, який буде видалено.",
            },
            follow_redirects=True,
        )
        # Find its id or delete by id
        from app.products.db import get_all_products
        all_p = get_all_products()
        temp_prod = [p for p in all_p if p["name"] == "Товар для видалення"][0]

        del_resp = self.client.post(
            f"/products/{temp_prod['id']}/delete",
            follow_redirects=True,
        )
        self.assertEqual(del_resp.status_code, 200)
        self.assertIn("успішно видалено".encode("utf-8"), del_resp.data)


if __name__ == "__main__":
    unittest.main()
