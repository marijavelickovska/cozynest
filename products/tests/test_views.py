from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from products.models import Product, Category
from products.forms import ProductForm


class AllProductsViewTest(TestCase):
    def setUp(self):
        self.url = reverse("products")

        self.cat1 = Category.objects.create(name="Category1")
        self.cat2 = Category.objects.create(name="Category2")

        Product.objects.create(
            name="Product1",
            base_price=10,
            category=self.cat1
        )
        Product.objects.create(
            name="Product2",
            base_price=20,
            category=self.cat2
        )

    def test_all_products_no_filters(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Product1")
        self.assertContains(response, "Product2")

    def test_all_products_category_filter(self):
        response = self.client.get(self.url, {"category": "Category1"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Product1")
        self.assertNotContains(response, "Product2")

    def test_all_products_search_query(self):
        response = self.client.get(self.url, {"q": "Product2"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Product2")
        self.assertNotContains(response, "Product1")

    def test_all_products_empty_search_redirect(self):
        response = self.client.get(self.url, {"q": ""})
        self.assertEqual(response.status_code, 302)


class AddProductViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="test123"
        )
        self.url = reverse("add_product")

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response.url)

    def test_logged_in_get_request(self):
        self.client.login(username="testuser", password="test123")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "products/product_managment.html")
        self.assertIsInstance(response.context["form"], ProductForm)
