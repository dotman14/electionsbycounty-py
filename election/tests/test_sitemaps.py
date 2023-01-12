from django.test import TestCase

from election.models import Candidate, County, ElectionData, Party, State
from election.sitemaps import (
    AllElectionTypes,
    AllStateCountyGovernorship,
    AllStateCountyPresidential,
    AllStateCountyResultGovernorship,
    AllStateCountyResultPresidential,
    ElectionsByCountyStatic,
)


class TestSitemaps(TestCase):
    def setUp(self) -> None:
        self.rep_party = Party.objects.create(
            party_name="Republican",
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

    def test_static_urls(self):
        static = ElectionsByCountyStatic()
        items = static.items()
        data = {}
        for _str in items:
            loc = static.location(_str)
            data[_str] = loc
        self.assertEqual(["home", "credit", "all_election_type"], items)
        self.assertEqual({"home": "/", "credit": "/credit", "all_election_type": "/result/"}, data)

    def test_all_election_types_url(self):
        e_types = AllElectionTypes()
        items = e_types.items()
        data = {}
        for _str in items:
            loc = e_types.location(_str)
            data[_str] = loc
        self.assertTrue(all(e_type in items for e_type in ["presidential"]))
        self.assertEqual({"presidential": "/result/presidential/"}, data)
        ElectionData.objects.create(
            election_type="Governorship",
            date_of_election=20161010,
            candidate=self.candidate,
            party=self.rep_party,
            area_type="County",
            area_name="Alameda",
            state=self.state,
            total_vote=99,
        )
        e_types = AllElectionTypes()
        items = e_types.items()
        data = {}
        for _str in items:
            loc = e_types.location(_str)
            data[_str] = loc
        self.assertTrue(all(e_type in items for e_type in ["presidential", "governorship"]))
        self.assertEqual(
            {"presidential": "/result/presidential/", "governorship": "/result/governorship/"}, data
        )

    def test_state_county_presidential(self):
        c_p = AllStateCountyPresidential()
        items = c_p.items()
        data = {}
        for _str in items:
            loc = c_p.location(_str)
            data[_str] = loc
        self.assertTrue(all(e_type in items for e_type in ["ca"]))
        self.assertEqual({"ca": "/result/presidential/ca/"}, data)

    def test_state_county_governorship(self):
        ElectionData.objects.create(
            election_type="Governorship",
            date_of_election=20161010,
            candidate=self.candidate,
            party=self.rep_party,
            area_type="County",
            area_name="Alameda",
            state=self.state,
            total_vote=99,
        )
        c_p = AllStateCountyGovernorship()
        items = c_p.items()
        data = {}
        for _str in items:
            loc = c_p.location(_str)
            data[_str] = loc
        self.assertTrue(all(e_type in items for e_type in ["ca"]))
        self.assertEqual({"ca": "/result/governorship/ca/"}, data)

    def test_all_state_county_result_presidential(self):
        r_p = AllStateCountyResultPresidential()
        items = r_p.items()
        data = {}
        for _str in items:
            loc = r_p.location(_str)
            data[_str] = loc
        self.assertTrue(all(e_type in items for e_type in [("ca", "alameda")]))
        self.assertEqual({("ca", "alameda"): "/result/presidential/ca/alameda"}, data)

    def test_all_state_county_result_governorship(self):
        ElectionData.objects.create(
            election_type="Governorship",
            date_of_election=20161010,
            candidate=self.candidate,
            party=self.rep_party,
            area_type="County",
            area_name="Alameda",
            state=self.state,
            total_vote=99,
        )
        r_p = AllStateCountyResultGovernorship()
        items = r_p.items()
        data = {}
        for _str in items:
            loc = r_p.location(_str)
            data[_str] = loc
        self.assertTrue(all(e_type in items for e_type in [("ca", "alameda")]))
        self.assertEqual({("ca", "alameda"): "/result/governorship/ca/alameda"}, data)
