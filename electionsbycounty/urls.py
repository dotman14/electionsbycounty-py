"""electionsbycounty URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from election.views import (
    ajax_get_county,
    all_county_for_state,
    all_election_type,
    all_state,
    credit,
    home,
    result,
    use,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", home, name="home"),
    path("credit", credit, name="credit"),
    path("getcounty/", ajax_get_county, name="auto-ajax"),
    path("use", use, name="use"),
    path(
        "result/<str:election_type>/<str:state_code>/",
        all_county_for_state,
        name="all_state_county",
    ),
    path(
        "result/<str:election_type>/",
        all_state,
        name="all_state",
    ),
    path(
        "result/",
        all_election_type,
        name="all_election_type",
    ),
    path(
        "result/<str:election_type>/<str:state_code>/<str:county>",
        result,
        name="result",
    ),
]


handler404 = "election.views.error_404"
handler500 = "election.views.error_500"
