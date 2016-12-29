# hnbex-python

[![Build Status](https://travis-ci.org/dobarkod/hnbex-python.svg?branch=master)](https://travis-ci.org/dobarkod/hnbex-python?branch=master)

A Python package for accessing hnbex.eu service

Installation
---------------------
Install the latest release of the package via pip:
```
pip install hnbex
```

Or install directly from GitHub repository:
```
git clone https://github.com/dobarkod/hnbex-python
cd hnbex-python
python setup.py install
```

Quickstart
---------------------
Get exchange rates valid on given date:
```
from datetime import date, timedelta
from hnbex import Rate
yesterday = date.today() - timedelta(1)
yesterday_rates_dict = Rate.get_rates(yesterday)
```

Get exchange rates valid today:
```
from hnbex import Rate
rates_dict = Rate.get_rates()
```

Get specific currency exchange rate:
```
euro = rates_dict.get('EUR')
```

Use the rate for conversion:
```
amount_eur = euro.from_hrk(500)
amount_hrk = euro.to_hrk(10)
```

How to run tests
---------------------

```
pip install tox
tox
```

License
---------------------

Copyright (C) 2016. Dobar Kod. Please see LICENSE file for details.
