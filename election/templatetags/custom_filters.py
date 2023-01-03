import datetime

from django import template

register = template.Library()


@register.filter(name="result_title")
def result_title(params: dict) -> str:
    title_str = (
        f"{params.get('election_type')} election results for "
        f"{params.get('county')} County, {params.get('state_code')}"
    )
    return title_str


@register.filter(name="result_title_breadcrumb")
def result_title_breadcrumb(params: dict):
    title_str = f"{params.get('state_code')}/{params.get('county')}"
    return title_str


@register.filter(name="str_to_date")
def str_to_date(value):
    return datetime.datetime.strptime(str(value), "%Y%m%d").date()


@register.filter(name="zip_to_list")
def zip_to_list(zipped_obj):
    return list(zipped_obj)
