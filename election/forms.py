from typing import Any, Dict, Tuple

from django.core.exceptions import ValidationError
from django.forms import CharField, ChoiceField, TextInput, forms

from election.models import ElectionData


class ElectionForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(ElectionForm, self).__init__(*args, **kwargs)

        for i, f in self.fields.items():
            self.fields[i].required = True
            if i == "election_type":
                f.widget.attrs["class"] = "form-select form-control-sm"
            if i == "county_state":
                f.widget.attrs["class"] = "form-control"

    election_type = ChoiceField(
        label="Type of Election", choices=ElectionData.ELECTION_TYPE, required=True
    )
    county_state = CharField(
        label="County-State", required=True, widget=TextInput(attrs={"autocomplete": "off"})
    )

    def clean(self) -> Dict[str, Any]:
        def split_county_state(c_s: str) -> Tuple:
            if c_s:
                _count_state = c_s.split(" | ")
                _state = _count_state[-1]
                if len(_state) != 2 or len(_count_state) < 2:
                    self.add_error(
                        "county_state",
                        ValidationError("Make sure you use 'County | ST' format"),
                    )
                _county = "-".join(_count_state[0:-1])
                return _county, _state

        cleaned_data = super().clean()
        county_state = cleaned_data.get("county_state")
        county, state = split_county_state(county_state)
        self.cleaned_data["county"] = county
        self.cleaned_data["state"] = state

        return cleaned_data
