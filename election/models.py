from django.db import models

# Create your models here.


class Party(models.Model):
    party_name = models.CharField(max_length=255)
    party_color_rgb = models.CharField(max_length=255)
    party_logo = models.CharField(max_length=255)


class State(models.Model):
    code = models.CharField("State Abbr.", max_length=2)
    state_name = models.CharField("Name of State", max_length=50)


class Candidate(models.Model):
    candidate_name = models.CharField(max_length=255)
    candidate_party = models.ForeignKey("Party", on_delete=models.CASCADE)
    candidate_image_path = models.CharField("Path to Candidate Image", max_length=255)


class ElectionData(models.Model):
    ELECTION_TYPE = [
        ("presidential", "Presidential"),
        ("governorship", "Governorship"),
    ]
    election_type = models.CharField("Election Type", max_length=30, choices=ELECTION_TYPE)
    date_of_election = models.IntegerField()
    candidate = models.ForeignKey("Candidate", on_delete=models.CASCADE)
    party = models.ForeignKey("Party", on_delete=models.CASCADE)
    area_type = models.CharField("Area Type", max_length=6, default="county")
    area_name = models.CharField("Area Name", max_length=255)
    state = models.ForeignKey("State", on_delete=models.CASCADE)
    total_vote = models.IntegerField()


class Quote(models.Model):
    quote_text = models.CharField("Quote Text", max_length=255)
    name = models.CharField("Name", max_length=100)
    quote_date = models.CharField("Date of Quote", max_length=50)

    def __str__(self):
        return f"{self.quote_text}, {self.name} ({self.quote_date})"
