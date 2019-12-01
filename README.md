# Predcis prediction model Case.

[![Python 3.7.4](https://img.shields.io/badge/python-3.7.4-blue.svg)](https://www.python.org/downloads/release/python-374/)

#### 1. To setup locally setup python environment and install dependencies.

`python -m venv .venv`

`pip install -r requirements.txt`

#### 2. If you have a custom csv you want to import you can use the command import.

`python manage.py import data <csv_file_path>`

- it takes a couple of seconds to import the data from scratch including weather data from dark sky.
  - 6000 entries for google ads data and 36 weather forecasts
- with bulk create it's not expensive to repopulate required data so all previous data
  will be deleted and replaced with new data, unless you have some error on new data, operation is aborted
  and old data remains.

- historical weather data would not be recreated it will just import new data if
  csv file has dates for which we don't have enough data.

### Usage

Here's an example of a get request to get a prediction for the account of id 5.

GET request to `http://localhost:8000/?account_id=5&date=2019-12-1`

- any additional data passed to query params would be disregarded.
- in case of wrong data format or type a value should show up.

### Our dummy model tries to do some prediction but I wouldn't trust him!!!

- TODO:
  - Write some tests.
