from unittest import TestCase

from election.templatetags.custom_filters import result_title


class TestTemplateTags(TestCase):
    def setUp(self) -> None:
        self.params = {"election_type": "Primary", "county": "Los Angeles", "state_code": "CA"}

    def test_result_title(self):
        expected_output = "Primary election results for Los Angeles County, CA"
        self.assertEqual(result_title(self.params), expected_output)
