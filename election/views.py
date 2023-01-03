import random

from django.http import (
    Http404,
    HttpResponseNotFound,
    HttpResponseRedirect,
    JsonResponse,
)
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from election.forms import ElectionForm
from election.models import County, ElectionData, ElectionNote, Quote, State

# Create your views here.


@require_http_methods(["GET", "POST"])
def home(request):
    quotes_pk = Quote.objects.values_list("pk", flat=True)
    quote_obj = Quote.objects.get(pk=random.choice(quotes_pk))
    if request.method == "POST":
        election_form_data = ElectionForm(request.POST)
        if election_form_data.is_valid():
            return HttpResponseRedirect(
                reverse(
                    "result",
                    kwargs={
                        "election_type": election_form_data.cleaned_data["election_type"],
                        "county": str(election_form_data.cleaned_data["county"]).lower(),
                        "state_code": str(election_form_data.cleaned_data["state"]).lower(),
                    },
                )
            )
        else:
            return render(
                request,
                "apps/election/index.html",
                {"quote_obj": quote_obj, "election_form": election_form_data},
            )
    election_form = ElectionForm()
    return render(
        request,
        "apps/election/index.html",
        {"quote_obj": quote_obj, "election_form": election_form},
    )


@require_http_methods(["GET"])
def ajax_get_county(request):
    query = request.GET.get("prefix", "")
    if query:
        county = County.objects.get_county_state(query)
        return JsonResponse({"success": county})
    else:
        return HttpResponseNotFound()


@require_http_methods(["GET"])
def result(request, election_type, state_code, county):
    _state_id = get_object_or_404(State, code__iexact=state_code)
    election = ElectionData.objects.get_election_data(election_type, county, _state_id)
    state_total_pct = ElectionData.objects.party_state_total(election_type, _state_id)
    notes = ElectionNote.objects.get_election_notes(election_type, county, _state_id)
    election_data = zip(election, state_total_pct, notes)
    return render(
        request,
        "apps/election/result.html",
        {
            "election_data": election_data,
            "params": {
                "election_type": str(election_type).capitalize(),
                "state_code": str(state_code).upper(),
                "county": str(county).title(),
            },
        },
    )


@require_http_methods(["GET"])
def credit(request):
    return render(request, "apps/election/credit.html")


@require_http_methods(["GET"])
def use(request):
    return render(request, "apps/election/use.html")


@require_http_methods(["GET"])
def all_county_for_state(request, election_type: str, state_code: str):
    _state_id = get_object_or_404(State, code__iexact=state_code)
    if not any([x[0] == election_type.lower() for x in ElectionData.ELECTION_TYPE]):
        print("Error")
    _county = ElectionData.objects.get_all_state_county(election_type, _state_id)
    return render(
        request,
        "apps/election/state_county.html",
        {"all_counties": _county, "state_code": state_code, "election_type": election_type},
    )


@require_http_methods(["GET"])
def all_state(request, election_type: str):
    if not any([x[0] == election_type.lower() for x in ElectionData.ELECTION_TYPE]):
        print("Error")
    _states = ElectionData.objects.get_all_state(election_type)
    return render(
        request,
        "apps/election/all_state.html",
        {"election_type": election_type, "states": _states},
    )


@require_http_methods(["GET"])
def all_election_type(request):
    _election_types = ElectionData.objects.get_all_election_type()
    return render(
        request,
        "apps/election/all_election_type.html",
        {"election_types": _election_types},
    )


def error_500(request):
    return render(request, "errors/500.html", status=500)


def error_404(request, exception):
    return render(request, "errors/404.html", status=404)
