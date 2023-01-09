from http import HTTPStatus

from django.test import TestCase
from django.test.utils import override_settings
from django.urls import reverse

from election.models import Quote


@override_settings(CACHE_MIDDLEWARE_SECONDS=0)
class TestViews(TestCase):
    def test_homepage(self):
        url = reverse("home")
        _response = self.client.get(url)
        self.assertEqual(_response.status_code, HTTPStatus.NOT_FOUND)
        Quote.objects.create(quote_text="I'll be back", quote_name="Terminator", quote_date="2099")
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIn("Lookup a county", response.content.decode("utf-8"))
        self.assertTemplateUsed(response, "apps/election/index.html")

    def test_credit_page(self):
        url = reverse("credit")
        _response = self.client.get(url)
        self.assertEqual(_response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(_response, "apps/election/credit.html")
