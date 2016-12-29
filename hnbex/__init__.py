import json
import re
import requests
from datetime import datetime
from decimal import Decimal


class Rate(object):

    RE_VALIDATION_DICT = {
        'currency_code': r'^[A-Z]{3}$',
        'buying_rate': r'^[0-9]+.[0-9]{6}$',
        'selling_rate': r'^[0-9]+.[0-9]{6}$',
        'median_rate': r'^[0-9]+.[0-9]{6}$',
    }

    URL = 'http://hnbex.eu/api/v1/rates/daily/'

    def __init__(self, currency_code, rate_date, buying_rate, selling_rate,
                 median_rate, unit_value):

        self._validate(currency_code, rate_date, buying_rate, selling_rate,
                       median_rate, unit_value)

        self.code = currency_code
        self.date = rate_date
        self.buy = Decimal(buying_rate)
        self.sell = Decimal(selling_rate)
        self.median = Decimal(median_rate)
        self.unit_value = unit_value

    def _validate(self, currency_code, rate_date, buying_rate, selling_rate,
                  median_rate, unit_value):

        for var, regex in self.RE_VALIDATION_DICT.items():
            if re.match(regex, eval(var)) is None:
                raise ValueError('{}: wrong format'.format(var))

        if unit_value not in [1, 100]:
            raise ValueError('unit_value must be 1 or 100')

    def from_hrk(self, amount_hrk):
        amount = Decimal(amount_hrk) / self.median * self.unit_value
        return amount.quantize(Decimal('0.000001'))

    def to_hrk(self, amount):
        amount_hrk = Decimal(amount) * self.median / self.unit_value
        return amount_hrk.quantize(Decimal('0.000001'))

    @classmethod
    def get_rates(cls, rate_date=None):

        if rate_date is None:
            rate_date = datetime.today()

        date_str = rate_date.strftime('%Y-%m-%d')
        result = requests.get(url=cls.URL, params={'date': date_str})

        if result.ok:
            rates = {}
            content = json.loads(result.content)
            for rate_dict in content:
                rate_dict['rate_date'] = rate_date
                try:
                    rates[rate_dict['currency_code']] = cls(**rate_dict)
                except (ValueError, KeyError):
                    continue
            return rates

        if 400 <= result.status_code < 500:
            raise ValueError("Server returned status code {}"
                             "".format(result.status_code))

        if 500 <= result.status_code < 600:
            raise IOError("Server returned status code {}"
                          "".format(result.status_code))
