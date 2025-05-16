from unittest import TestCase
import datetime
from app.domain.utils.parse_datetime_to_string import parse_datetime_to_Mercadopago_date_format


class TestParseDatetimeToString(TestCase):

    def test_datetime_parse_works_successfully(self):
        target_date = datetime.datetime(
            day=10, month=3, year=2012, hour=12, minute=12, second=12)
        parsed_date = parse_datetime_to_Mercadopago_date_format(target_date)

        self.assertIsInstance(parsed_date, str)
        self.assertEqual(parsed_date, "20120310 12:12:12")
