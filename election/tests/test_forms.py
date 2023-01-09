from django.http import HttpRequest
from django.test import Client, TestCase
from django.urls import reverse

from election.forms import ElectionForm
from election.models import Candidate, County, ElectionData, Party, Quote, State


class TestElectionForm(TestCase):
    def setUp(self) -> None:
        self.request = HttpRequest()
        Quote.objects.create(quote_text="I'll be back", quote_name="Terminator", quote_date="2099")

        self.party = Party.objects.create(
            party_name="test party",
            party_logo="path/to/logo.png",
            party_color_rgb="rgb(2, 3, 4)",
        )

        self.state = State.objects.create(
            code="IN",
            state_name="Indiana",
        )

        self.ca_id = State.objects.filter(code="IN").values_list("id", flat=True).first()

        self.county = County.objects.create(
            state=self.state,
            county_name="Monroe",
        )

        self.candidate = Candidate.objects.create(
            candidate_name="John, Doe",
            candidate_party=self.party,
            candidate_image_path="candidate.png",
        )

        self.election_data = ElectionData.objects.create(
            election_type="Presidential",
            date_of_election=21212,
            candidate=self.candidate,
            party=self.party,
            area_type="County",
            area_name="Monroe",
            state=self.state,
            total_vote=2999,
        )

    def test_empty_form(self):
        form = ElectionForm()
        self.assertIn("presidential", str(form))
        self.assertNotIn("senate", str(form))
        self.assertIn("election_type", form.fields)
        self.assertIn("county_state", form.fields)

    def test_invalid_electiondata_form(self):
        _invalid_format = ElectionForm(
            {
                "election_type": "presidential",
                "county_state": "test",
            }
        )
        self.assertIn(
            "Make sure you use County | ST format", _invalid_format.errors.get("county_state")
        )

        _empty_format = ElectionForm(
            {
                "election_type": "",
                "county_state": "",
            }
        )
        self.assertTrue(
            all(field in _empty_format.errors.keys() for field in ["election_type", "county_state"])
        )

    def test_valid_electiondata_form(self):
        _valid_format = ElectionForm(
            {
                "election_type": "presidential",
                "county_state": "Monroe | IN",
            }
        )

        self.assertTrue(_valid_format.is_valid())
        d = Client().post(
            reverse("home"),
            data={
                "election_type": "presidential",
                "county_state": "Monroe | IN",
            },
        )
        self.assertEqual(d.status_code, 302)
        self.assertEqual(d["Location"], "/result/presidential/in/monroe")
