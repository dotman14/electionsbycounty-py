from django.test import TestCase

from election.forms import ElectionForm


class TestElectionForm(TestCase):
    def test_empty_form(self):
        form = ElectionForm()
        self.assertIn("presidential", str(form))
        self.assertNotIn("senate", str(form))
        self.assertIn("election_type", form.fields)
        self.assertIn("county_state", form.fields)
