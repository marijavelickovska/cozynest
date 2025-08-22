from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from profiles.forms import UserUpdateForm, UserProfileForm


class ProfileViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="test123"
        )
        self.profile = self.user.userprofile
        self.url = reverse("profile")

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response.url)

    def test_profile_tab_get(self):
        self.client.login(username="testuser", password="test123")
        response = self.client.get(reverse("profile"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "profiles/profile_base.html")
        self.assertIsInstance(response.context["form"], UserUpdateForm)

    def test_delivery_information_tab_get(self):
        self.client.login(username="testuser", password="test123")
        response = self.client.get(reverse("delivery_information"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "profiles/profile_base.html")
        self.assertIsInstance(response.context["form"], UserProfileForm)

    def test_order_history_tab_get(self):
        self.client.login(username="testuser", password="test123")
        response = self.client.get(reverse("order_history"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "profiles/profile_base.html")
        self.assertQuerysetEqual(response.context["orders"], [])
