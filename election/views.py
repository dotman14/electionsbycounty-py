import random

from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from election.models import Quote

# Create your views here.


def home(request):
    quotes_pk = Quote.objects.values_list("pk", flat=True)
    quote_obj = Quote.objects.get(pk=random.choice(quotes_pk))
    return render(request, "apps/election/index.html", {"quote_obj": quote_obj})


@require_http_methods(["GET"])
def credit(request):
    return render(request, "apps/election/credit.html")


@require_http_methods(["GET"])
def use(request):
    return render(request, "apps/election/use.html")
