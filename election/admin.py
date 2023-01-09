from django.contrib import admin

from election.models import (
    Candidate,
    County,
    ElectionData,
    ElectionNote,
    Party,
    Quote,
    State,
)

# Register your models here.

admin.site.register(Party)
admin.site.register(Candidate)
admin.site.register(State)
admin.site.register(County)
admin.site.register(ElectionData)
admin.site.register(ElectionNote)
admin.site.register(Quote)
