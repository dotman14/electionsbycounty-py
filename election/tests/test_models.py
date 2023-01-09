from http import HTTPStatus

import pytest
from django.test import TestCase
from django.test.utils import override_settings
from django.urls import reverse

from election.models import (
    Candidate,
    County,
    ElectionData,
    ElectionNote,
    Party,
    Quote,
    State,
)


@override_settings(CACHE_MIDDLEWARE_SECONDS=0)
class TestModels(TestCase):
    def setUp(self):
        self.rep_party = Party.objects.create(
            party_name="Republican",
            party_logo="path/to/logo.png",
            party_color_rgb="rgb(2, 3, 4)",
        )
        self.dem_party = Party.objects.create(
            party_name="Democratic",
            party_logo="path/to/logo.png",
            party_color_rgb="rgb(2, 3, 4)",
        )

        self.state = State.objects.create(
            code="CA",
            state_name="California",
        )

        self.ca_id = State.objects.filter(code="CA").values_list("id", flat=True).first()

        self.county = County.objects.create(
            state=self.state,
            county_name="Alameda",
        )

        self.candidate = Candidate.objects.create(
            candidate_name="John, Doe",
            candidate_party=self.rep_party,
            candidate_image_path="candidate.png",
        )

        self.quote = Quote.objects.create(
            quote_text="I'll be back", quote_name="Terminator", quote_date="2099"
        )

        self.election_note = ElectionNote.objects.create(
            election_type="Presidential",
            date_of_election=20161010,
            area_type="County",
            area_name="Alameda",
            state=self.state,
            election_notes="Write-in votes",
        )

        self.election_data = ElectionData.objects.create(
            election_type="Presidential",
            date_of_election=20161010,
            candidate=self.candidate,
            party=self.rep_party,
            area_type="County",
            area_name="Alameda",
            state=self.state,
            total_vote=2999,
        )

        self.dem_candidate = Candidate.objects.create(
            candidate_name="John, Doe Mary",
            candidate_party=self.dem_party,
            candidate_image_path="candidate.png",
        )

        ElectionData.objects.create(
            election_type="Presidential",
            date_of_election=20161010,
            candidate=self.dem_candidate,
            party=self.dem_party,
            area_type="County",
            area_name="Alameda",
            state=self.state,
            total_vote=230,
        )

        ElectionData.objects.create(
            election_type="Presidential",
            date_of_election=20161010,
            candidate=None,
            party=None,
            area_type="County",
            area_name="Alameda",
            state=self.state,
            total_vote=230,
        )

    def test_election_data_model(self):
        self.assertEqual(self.election_data.state, self.state)
        self.assertEqual(self.election_data.candidate, self.candidate)
        self.assertEqual(self.election_data.party, self.rep_party)
        self.assertEqual(self.election_data.total_vote, 2999)

    def test_election_data_str(self):
        self.assertEqual(
            str(self.election_data),
            f"Presidential Alameda {self.rep_party} 20161010 CA 2999 {self.candidate}",
        )

    def test_election_data_get_all_election_type(self):
        all_election_type = ElectionData.objects.get_all_election_type()
        self.assertEqual(len(all_election_type), 1)
        self.assertEqual(
            [dicts.get("election_type") for dicts in all_election_type], ["Presidential"]
        )

        ElectionData.objects.create(
            election_type="Governorship",
            date_of_election=20161010,
            candidate=self.candidate,
            party=self.rep_party,
            area_type="County",
            area_name="Alameda",
            state=self.state,
            total_vote=1000,
        )
        all_election_type = ElectionData.objects.get_all_election_type()
        self.assertEqual(len(all_election_type), 2)
        self.assertEqual(
            [dicts.get("election_type") for dicts in all_election_type],
            ["Governorship", "Presidential"],
        )

    def test_election_data_get_all_state(self):
        all_states = ElectionData.objects.get_all_state("Presidential")
        self.assertEqual([dicts.get("state__state_name") for dicts in all_states], ["California"])

    def test_election_get_all_state_county(self):
        ElectionData.objects.create(
            election_type="Presidential",
            date_of_election=20161010,
            candidate=self.candidate,
            party=self.rep_party,
            area_type="County",
            area_name="Monroe",
            state=self.state,
            total_vote=1000,
        )
        state_county = ElectionData.objects.get_all_state_county("Presidential", self.ca_id)
        self.assertEqual([dicts.get("area_name") for dicts in state_county], ["Alameda", "Monroe"])

    def test_party_model(self):
        self.assertEqual(self.rep_party.party_name, "Republican")
        self.assertEqual(self.rep_party.party_logo, "path/to/logo.png")
        self.assertEqual(self.rep_party.party_color_rgb, "rgb(2, 3, 4)")

    def test_state_model(self):
        self.assertEqual(self.state.state_name, "California")
        with pytest.raises(Exception):
            State.objects.get(code="TX")

    def test_county_model(self):
        self.assertEqual(self.county.state.state_name, "California")
        self.assertEqual(self.county.state.code, "CA")
        self.assertEqual(self.county.county_name, "Alameda")

    def test_county_str(self):
        self.assertEqual(str(self.county), "Alameda-CA")

    def test_county_manager(self):
        County.objects.create(
            state=self.state,
            county_name="Alameda2",
        )
        self.assertEqual(County.objects.get_county_state("Alameda2"), ["Alameda2 | CA"])
        self.assertTrue(len(County.objects.get_county_state("Alam")) == 2)
        self.assertEqual(County.objects.get_county_state("Alam"), ["Alameda | CA", "Alameda2 | CA"])
        self.assertIsNone(County.objects.get_county_state("Geor"))

    def test_candidate_model(self):
        self.assertEqual(self.candidate.candidate_name, "John, Doe")
        self.assertEqual(self.candidate.candidate_party, self.rep_party)
        self.assertEqual(self.candidate.candidate_image_path, "candidate.png")

    def test_quote_model(self):
        self.assertEqual(self.quote.quote_text, "I'll be back")
        self.assertEqual(self.quote.quote_name, "Terminator")
        self.assertEqual(self.quote.quote_date, "2099")

    def test_quote_str(self):
        self.assertEqual(str(self.quote), "I'll be back, Terminator (2099)")

    def test_election_note(self):
        self.assertEqual(self.election_note.election_notes, "Write-in votes")
        self.assertEqual(self.election_note.state.state_name, "California")
        self.assertEqual(
            ElectionNote.objects.filter(area_type="Governorship", area_name="Cook").count(), 0
        )

    def test_election_note_manager(self):
        election_note = ElectionNote.objects.get_election_notes(
            "Presidential", "Alameda", self.ca_id
        )[0]
        self.assertEqual(
            election_note, {"date_of_election": 20161010, "election_notes": "Write-in votes"}
        )

    def test_election_party_state_total(self):
        election_total = ElectionData.objects.party_state_total("Presidential", self.ca_id)
        self.assertIn(
            2999, [_total.get("total_stats")[0][0].get("Republican") for _total in election_total]
        )
        self.assertIn(
            230, [_total.get("total_stats")[1][0].get("Democratic") for _total in election_total]
        )
        self.assertEqual([_total.get("state_total") for _total in election_total], [3459])

    def test_election_data_get_election_data(self):
        election_total = ElectionData.objects.get_election_data(
            "Presidential", "Alameda", self.ca_id
        )
        self.assertEqual(len(election_total[0].get("vote_data")), 3)

    def test_election_data_all_election_type_view(self):
        url = reverse("all_election_type")
        _response = self.client.get(url)
        self.assertInHTML(
            '<a href="/result/presidential/">Presidential</a>', _response.content.decode()
        )

    def test_election_data_all_state_view(self):
        url = reverse("all_state", kwargs={"election_type": "presidential"})
        _response = self.client.get(url)
        self.assertInHTML(
            '<a href="/result/presidential/ca/">California</a>', _response.content.decode()
        )
        _url_404 = reverse("all_state", kwargs={"election_type": "senate"})
        _response_404 = self.client.get(_url_404)
        self.assertEqual(_response_404.status_code, HTTPStatus.NOT_FOUND)

    def test_election_data_all_county_for_state_view(self):
        url = reverse(
            "all_state_county", kwargs={"election_type": "presidential", "state_code": "CA"}
        )
        _response = self.client.get(url)
        self.assertInHTML(
            '<a href="/result/presidential/CA/alameda">Alameda</a>', _response.content.decode()
        )
        invalid_election_type = reverse(
            "all_state_county", kwargs={"election_type": "senate", "state_code": "CA"}
        )
        _response_404 = self.client.get(invalid_election_type)
        self.assertEqual(_response_404.status_code, HTTPStatus.NOT_FOUND)
        self.state = State.objects.create(
            code="NY",
            state_name="New York",
        )
        invalid_no_result = reverse(
            "all_state_county", kwargs={"election_type": "presidential", "state_code": "NY"}
        )
        _response_empty = self.client.get(invalid_no_result)
        self.assertEqual(_response_empty.status_code, HTTPStatus.NOT_FOUND)

    def test_election_data_ajax_get_county(self):
        response = self.client.get(reverse("auto-ajax"), {"prefix": "al"})
        self.assertEqual(["Alameda | CA"], response.json().get("success"))
        _response = self.client.get(reverse("auto-ajax"), {"prefix": ""})
        self.assertEqual(_response.status_code, HTTPStatus.NOT_FOUND)

    def test_election_data_result_view(self):
        url = reverse(
            "result",
            kwargs={"election_type": "presidential", "state_code": "CA", "county": "alameda"},
        )
        response = self.client.get(url)
        self.assertInHTML(
            '<span class="yearDisplay">Oct. 10, 2016</span>', response.content.decode()
        )
        self.assertInHTML("John, Doe Mary", response.content.decode())
        self.assertInHTML("2,999", response.content.decode())
        _url_404 = reverse("result", kwargs={"election_type": "presidential", "state_code": "NY", "county": "new york"})
        _response_404 = self.client.get(_url_404)
        self.assertEqual(_response_404.status_code, HTTPStatus.NOT_FOUND)
