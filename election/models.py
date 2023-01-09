from django.contrib.postgres.aggregates import ArrayAgg
from django.db import models
from django.db.models import Case, Count, ExpressionWrapper, F, FloatField, Sum, When
from django.db.models.functions import Round

# Create your models here.


class Party(models.Model):
    party_name = models.CharField(max_length=255)
    party_color_rgb = models.CharField(max_length=255)
    party_logo = models.CharField(max_length=255)


class State(models.Model):
    code = models.CharField("State Abbr.", max_length=2)
    state_name = models.CharField("Name of State", max_length=50)


class CountyManager(models.Manager):
    def get_county_state(self, county_prefix):
        county_objects = self.select_related("state").filter(county_name__icontains=county_prefix)
        if county_objects:
            return [
                f"{county_object.county_name} | {county_object.state.code}"
                for county_object in county_objects
            ]


class County(models.Model):
    state = models.ForeignKey("State", on_delete=models.CASCADE, related_name="state")
    county_name = models.CharField("County Name", max_length=255)
    objects = CountyManager()

    def __str__(self):
        return f"{self.county_name}-{self.state.code}"


class Candidate(models.Model):
    candidate_name = models.CharField(max_length=255)
    candidate_party = models.ForeignKey("Party", on_delete=models.CASCADE)
    candidate_image_path = models.CharField("Path to Candidate Image", max_length=255)


class ElectionDataManager(models.Manager):
    def get_election_data(self, election_type, county, state_id):
        _data = (
            self.select_related("candidate")
            .select_related("party")
            .values("date_of_election", "election_type", "area_name", "area_type")
            .filter(
                election_type__iexact=election_type, area_name__iexact=county, state_id=state_id
            )
            .annotate(cand_ids=ArrayAgg("candidate__candidate_name"))
            .annotate(cand_images=ArrayAgg("candidate__candidate_image_path"))
            .annotate(all_votes=ArrayAgg("total_vote"))
            .annotate(party_ids=ArrayAgg("party__party_name"))
            .annotate(party_color=ArrayAgg("party__party_color_rgb"))
            .annotate(party_logo=ArrayAgg("party__party_logo"))
            .order_by("-date_of_election")
        )
        sorted_list = []
        for data in _data:
            sorted_list.append(
                {
                    "date_of_election": data["date_of_election"],
                    "election_type": data["election_type"],
                    "area_name": data["area_name"],
                    "vote_data": sorted(
                        list(
                            zip(
                                data["all_votes"],
                                data["cand_ids"],
                                data["party_ids"],
                                data["cand_images"],
                                data["party_color"],
                                data["party_logo"],
                            )
                        ),
                        key=lambda x: x[0] if x[0] else 0,
                        reverse=True,
                    ),
                }
            )
        return sorted_list

    def party_state_total(self, election_type, state_id):
        _data = (
            self.values("date_of_election")
            .filter(election_type__iexact=election_type, state_id=state_id)
            .annotate(
                republican=Sum(
                    Case(When(party__party_name="Republican", then=F("total_vote")), default=0)
                ),
                democratic=Sum(
                    Case(When(party__party_name="Democratic", then=F("total_vote")), default=0)
                ),
            )
            .annotate(state_total_all=Sum("total_vote"))
            .annotate(state_total_other=F("state_total_all") - (F("republican") + F("democratic")))
            .annotate(
                republican_pct=ExpressionWrapper(
                    Round(F("republican") * 100.0 / F("state_total_all"), 2),
                    output_field=FloatField(),
                )
            )
            .annotate(
                democratic_pct=ExpressionWrapper(
                    Round(F("democratic") * 100.0 / F("state_total_all"), 2),
                    output_field=FloatField(),
                )
            )
            .annotate(
                rest_pct=ExpressionWrapper(
                    Round(100 - (F("republican_pct") + F("democratic_pct")), 2),
                    output_field=FloatField(),
                )
            )
            .order_by("-date_of_election")
        )
        sorted_list = []
        for data in _data:
            sorted_list.append(
                {
                    "state_total": data["state_total_all"],
                    "total_stats": sorted(
                        list(
                            zip(
                                [
                                    {"Republican": data["republican"]},
                                    {"Democratic": data["democratic"]},
                                    {"Others": data["state_total_other"]},
                                ],
                                [data["republican_pct"], data["democratic_pct"], data["rest_pct"]],
                            )
                        ),
                        key=lambda x: x[1],
                        reverse=True,
                    ),
                }
            )
        return sorted_list

    def get_all_state_county(self, election_type, state_code):
        return (
            self.values("area_name")
            .filter(state=state_code, election_type__iexact=election_type)
            .annotate(Count("id"))
            .order_by("area_name")
        )

    def get_all_state(self, election_type):
        return (
            self.select_related("state")
            .values("state__state_name", "state__code")
            .filter(election_type__iexact=election_type)
            .annotate(Count("id"))
            .order_by("state")
        )

    def get_all_election_type(self):
        return self.values("election_type").annotate(Count("id")).order_by("election_type")


class ElectionData(models.Model):
    class Meta:
        ordering = ["-date_of_election", "-total_vote"]

    ELECTION_TYPE = [
        ("presidential", "Presidential"),
        ("governorship", "Governorship"),
    ]
    election_type = models.CharField("Election Type", max_length=30, choices=ELECTION_TYPE)
    date_of_election = models.IntegerField()
    candidate = models.ForeignKey(
        "Candidate", on_delete=models.CASCADE, null=True, related_name="candidate"
    )
    party = models.ForeignKey("Party", on_delete=models.CASCADE, null=True, related_name="party")
    area_type = models.CharField("Area Type", max_length=6, default="county")
    area_name = models.CharField("Area Name", max_length=255)
    state = models.ForeignKey("State", on_delete=models.CASCADE)
    total_vote = models.IntegerField(null=True)
    objects = ElectionDataManager()

    def __str__(self):
        return (
            f"{self.election_type} {self.area_name} {self.party} {self.date_of_election} "
            f"{self.state.code} {self.total_vote} {self.candidate}"
        )


class Quote(models.Model):
    quote_text = models.CharField("Quote Text", max_length=255)
    quote_name = models.CharField("Name", max_length=100)
    quote_date = models.CharField("Date of Quote", max_length=50)

    def __str__(self):
        return f"{self.quote_text}, {self.quote_name} ({self.quote_date})"


class ElectionNoteManager(models.Manager):
    def get_election_notes(self, election_type, county, state_id):
        return (
            self.values("date_of_election", "election_notes")
            .filter(
                election_type__iexact=election_type, area_name__iexact=county, state_id=state_id
            )
            .order_by("-date_of_election")
        )


class ElectionNote(models.Model):
    ELECTION_TYPE = [
        ("presidential", "Presidential"),
        ("governorship", "Governorship"),
    ]
    election_type = models.CharField("Election Type", max_length=30, choices=ELECTION_TYPE)
    date_of_election = models.IntegerField()
    area_type = models.CharField("Area Type", max_length=6, default="county")
    area_name = models.CharField("Area Name", max_length=255)
    state = models.ForeignKey("State", on_delete=models.CASCADE)
    election_notes = models.TextField("Election Notes", null=True)
    objects = ElectionNoteManager()
