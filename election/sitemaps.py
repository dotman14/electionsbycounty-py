from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from election.models import ElectionData


class ElectionsByCountyStatic(Sitemap):
    def items(self):
        return ["home", "credit", "all_election_type"]

    def location(self, item):
        return reverse(item)


class AllElectionTypes(Sitemap):
    def items(self):
        election_type = ElectionData.objects.get_all_election_type()
        _election_type = [str(b.get("election_type")).lower() for b in election_type]
        return _election_type

    def location(self, _election_type):
        return reverse("all_state", args=[_election_type])


class AllStateCountyPresidential(Sitemap):
    def items(self):
        all_state = ElectionData.objects.get_all_state("presidential")
        _all_state = [str(b.get("state__code")).lower() for b in all_state]
        return _all_state

    def location(self, _all_state):
        return reverse(
            "all_state_county", kwargs={"election_type": "presidential", "state_code": _all_state}
        )


class AllStateCountyGovernorship(Sitemap):
    def items(self):
        all_state = ElectionData.objects.get_all_state("governorship")
        _all_state = [str(b.get("state__code")).lower() for b in all_state]
        return _all_state

    def location(self, _all_state):
        return reverse(
            "all_state_county", kwargs={"election_type": "governorship", "state_code": _all_state}
        )


class AllStateCountyResultPresidential(Sitemap):
    def items(self):
        all_state_county_president = ElectionData.objects.get_state_county_sitemap("presidential")
        _all_state_county_president = [
            (str(b.get("state__code")).lower(), str(b.get("area_name")).lower())
            for b in all_state_county_president
        ]
        return _all_state_county_president

    def location(self, _all_state_county_president):
        return reverse(
            "result",
            kwargs={
                "election_type": "presidential",
                "state_code": _all_state_county_president[0],
                "county": _all_state_county_president[1],
            },
        )


class AllStateCountyResultGovernorship(Sitemap):
    def items(self):
        all_state_county_governorship = ElectionData.objects.get_state_county_sitemap(
            "governorship"
        )
        _all_state_county_governorship = [
            (str(b.get("state__code")).lower(), str(b.get("area_name")).lower())
            for b in all_state_county_governorship
        ]
        return _all_state_county_governorship

    def location(self, _all_state_county_governorship):
        return reverse(
            "result",
            kwargs={
                "election_type": "governorship",
                "state_code": _all_state_county_governorship[0],
                "county": _all_state_county_governorship[1],
            },
        )
