# czech-covid19-data-api
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

API wrapper for official covid19 data. Written in Python. Data source https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19. 

## Installation
Just use:
```
pip install covid-19-api
```

## How to use

Example 1: Get data in JSON format:

```
from covid19_api.src import api

if __name__ == "__main__":
    (status, data) = api.get_deaths_overview()

    if status:
        print(data)
```

Example 2: Get data in CSV format:

```
from covid19_api.src import api

if __name__ == "__main__":
    (status, data) = api.get_deaths_overview(resource="/umrti.csv")

    if status:
        print(data)
```
