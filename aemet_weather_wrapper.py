import requests
import json
import weather_config as cfg
from datetime import datetime


def config(new_api_key):
    if check_connection(new_api_key):
        cfg.api_key = new_api_key


def check_connection(api_key):
    if api_key == "":
        raise Exception("API Key is blank. Check 'weather_config.py.")
    else:
        r = requests.get('https://opendata.aemet.es/opendata/api/maestro/municipios', headers={"api_key": api_key})
        if r.status_code == 200:
            print("API Key and connection OK")
            return True
        else:
            print("Request returned " + str(r.status_code))
            raise Exception("Request returned" + str(r.status_code))


def external_help():  # Downloads and shows AEMET's OpenData JSON. No API Key needed.
    r = requests.get("https://opendata.aemet.es/AEMET_OpenData_specification.json")
    print(r.text)


def get_forecast_daily_from_code(city_code):  # It's better to use this way to get the forecast.
    r = requests.get("https://opendata.aemet.es/opendata/api/prediccion/especifica/municipio/diaria/" + str(city_code),
                     headers={"api_key": cfg.api_key})
    data_json_url = json.loads(r.text)
    response_dict = json.loads(requests.get(data_json_url.get("datos")).text)
    update_time = datetime.strptime(response_dict[0]("elaborado"), "%Y-%m-%dT%H:%M:%S")
    sections = {}
    # Here I thought it would be better to have a more graphical approach, avoiding for loops and showing how the
    # AEMET API delivers the data. It may look clunkier and I'm open to change it.
    for x in len(response_dict[0]("prediccion")("dia")):
        sections[(response_dict[0]("prediccion")[x]("fecha")).removesuffix("T00:00:00")]

    new_forecast = Forecast(response_dict.get("nombre"), city_code, True, update_time, sections)
    return new_forecast


class Forecast:
    def __init__(self, city_name, city_code, is_daily, update_time, sections):
        self.city_name = city_name
        self.city_code = city_code
        self.is_daily = is_daily
        self.update_time = update_time
        self.sections = sections

    @classmethod
    def refresh_forecast(self):
        pass


get_forecast_daily_from_code(26011)
