import datetime
import json
import unittest
from decimal import Decimal
from hnbex import Rate

try:
    from mock import patch
except ImportError:
    from unittest.mock import patch


SAMPLE_EUR_RATE = {"unit_value": 1,
                   "buying_rate": "7.507742",
                   "selling_rate": "7.552924",
                   "currency_code": "EUR",
                   "median_rate": "7.530333"}

TEST_200 = 'http://hnbex.eu/api/v1/rates/daily/200'
TEST_500 = 'http://hnbex.eu/api/v1/rates/daily/500'
TEST_400 = 'http://hnbex.eu/api/v1/rates/daily/400'


class FakeRequest(object):

    def __init__(self, url, params):

        status = 200
        if url == TEST_400:
            status = 400
        elif url == TEST_500:
            status = 500

        self.ok = status == 200
        self.content = json.dumps([SAMPLE_EUR_RATE])
        self.status_code = status


class TestRate(unittest.TestCase):

    def setUp(self):
        self.rate_date = datetime.date(2016, 12, 28)

        rate_dict = SAMPLE_EUR_RATE.copy()
        rate_dict.update({"rate_date": self.rate_date})
        self.rate = Rate(**rate_dict)

    def test_conversion_from_hrk(self):
        self.assertEqual(self.rate.from_hrk(30), Decimal('3.983888'))

    def test_conversion_to_hrk(self):
        self.assertEqual(self.rate.to_hrk(Decimal(4)), Decimal('30.121332'))

    def test_get_rates_4xx(self):

        with patch('requests.get', FakeRequest):
            Rate.URL = TEST_400
            self.assertRaises(ValueError, Rate.get_rates)

    def test_get_rates_5xx(self):

        with patch('requests.get', FakeRequest):
            Rate.URL = TEST_500
            self.assertRaises(IOError, Rate.get_rates)

    def test_get_rates(self):

        with patch('requests.get', FakeRequest):
            Rate.URL = TEST_200
            rates = Rate.get_rates(self.rate_date)

            self.assertIn('EUR', rates)
            self.assertEqual(rates['EUR'].__dict__, self.rate.__dict__)

if __name__ == '__main__':
    unittest.main()
