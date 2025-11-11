from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Car, Manufacturer


class PublicViewsTests(TestCase):
    def test_index(self):
        url = reverse("taxi:index")
        response = self.client.get(url)
        self.assertNotEquals(response.status_code, 200)


class PrivateViewsTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpassword",
        )
        self.client.force_login(self.user)

    def test_index_content(self):
        url = reverse("taxi:index")
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_retrieve_manufacturer_list(self):
        Car.objects.create(
            model="Test Car",
            manufacturer=Manufacturer.objects.create(
                name="Test Manufacturer",
                country="Test Country"
            )
        )
        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, "Test Manufacturer")
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")
        manufacturer = Manufacturer.objects.all()
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturer)
        )
