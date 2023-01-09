import datetime

from django.test import TestCase

from election.templatetags.custom_filters import result_title, str_to_date, zip_to_list


class TestTemplateTags(TestCase):
    def setUp(self) -> None:
        self.params = {"election_type": "Primary", "county": "Los Angeles", "state_code": "CA"}

    def test_result_title(self):
        expected_output = "Primary election results for Los Angeles County, CA"
        self.assertEqual(result_title(self.params), expected_output)

    def test_str_to_date(self):
        self.assertEqual(str_to_date("20210701"), datetime.date(2021, 7, 1))
        self.assertEqual(str_to_date("20210115"), datetime.date(2021, 1, 15))

    def test_zip_to_list(self):
        self.assertEqual(
            zip_to_list(zip([1, 2, 3], ["a", "b", "c"])), [(1, "a"), (2, "b"), (3, "c")]
        )
        self.assertEqual(
            zip_to_list(zip(["a", "b", "c"], [1, 2, 3])), [("a", 1), ("b", 2), ("c", 3)]
        )
        self.assertEqual(zip_to_list(zip([], [])), [])
