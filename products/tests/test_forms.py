from django.test import TestCase
from products.forms import ProductForm
from django.core.files.uploadedfile import SimpleUploadedFile


class ProductFormTest(TestCase):
    def test_product_form_valid_data(self):
        image = SimpleUploadedFile(
            name="test.jpg", content=b"file_content", content_type="image/jpeg"
        )
        form_data = {
            "name": "Test Product",
            "base_price": 10.99,
            "description": "Some description",
        }
        form_files = {"image": image}
        form = ProductForm(data=form_data, files=form_files)
        self.assertTrue(form.is_valid())

    def test_product_form_placeholder(self):
        form = ProductForm()
        self.assertIn("placeholder", form.fields["name"].widget.attrs)
        self.assertIn("placeholder", form.fields["description"].widget.attrs)
        self.assertIn("placeholder", form.fields["base_price"].widget.attrs)
