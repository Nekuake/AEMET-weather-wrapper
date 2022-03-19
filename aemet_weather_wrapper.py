import requests
import json
import weather_config as cfg
from datetime import datetime
import os


def config(new_api_key):
    if check_connection(new_api_key):
        os.environ["AEMET_APIKEY"] = new_api_key


def check_connection(api_key):
    if api_key == "":
        raise Exception("API Key is blank. Check 'weather_config.py.")
    else:
        r = requests.get('https://opendata.aemet.es/opendata/api/maestro/municipios', headers={"api_key": api_key})
        if r.status_code == 200:
            print("API Key and connection OK")
            return True
        else:
            raise Exception("Request returned" + str(r.status_code))


def external_help():  # Downloads and shows AEMET's OpenData JSON. No API Key needed.
    r = requests.get("https://opendata.aemet.es/AEMET_OpenData_specification.json")
    print(r.text)


def get_forecast_daily_from_code(city_code):  # It's better to use this way to get the forecast.
    if os.getenv("AEMET_APIKEY")==None:
        raise Exception("No API Key saved. Please run 'config(API_KEY)'")
    r = requests.get("https://opendata.aemet.es/opendata/api/prediccion/especifica/municipio/diaria/" + str(city_code),
                     headers={"api_key": os.getenv("AEMET_APIKEY")})

    data_json_url = json.loads(r.text)
    response_dict = json.loads(requests.get(data_json_url.get("datos")).text)
    update_time = datetime.strptime(response_dict[0]["elaborado"], "%Y-%m-%dT%H:%M:%S")
    sections = {}
    # Here I thought it would be better to have a more graphical approach, avoiding for loops and showing how the
    # AEMET API delivers the data. It may look clunkier, so I'm open to change it.
    for day in (response_dict[0]["prediccion"]["dia"]):
        aux_date = day["fecha"].removesuffix("T00:00:00")

        sections[aux_date] = {}
        for period in (day["probPrecipitacion"]):
            try:
                sections[aux_date][period["periodo"]] = {}
                sections[aux_date][period["periodo"]]["rainfall_probability"] = period["value"]
            except KeyError:
                # AEMET will not populate any timestamps after Day 4, just the value, so we'll implement it. This is
                # not the most beautiful way but I am focused in dumping the whole forecast.
                sections[aux_date]["00-24"] = {}
                sections[aux_date]["00-24"]["rainfall_probability"] = period["value"]
        for period in (day["estadoCielo"]):
            try:
                sections[aux_date][period["periodo"]]["weather_code"] = cfg.status_weather_codes[period["value"][0:2]]
            except KeyError:
                sections[aux_date]["00-24"]["weather_code"] = cfg.status_weather_codes[period["value"][0:2]]
        for period in (day["cotaNieveProv"]):
            try:
                sections[aux_date][period["periodo"]]["snow_level"] = period["value"]
            except KeyError:
                sections[aux_date]["00-24"]["snow_level"] = period["value"]
        for period in (day["rachaMax"]):
            try:
                sections[aux_date][period["periodo"]]["wind_gusts"] = period["value"]
            except KeyError:
                sections[aux_date]["00-24"]["wind_gusts"] = period["value"]
        for period in (day["viento"]):
            try:
                sections[aux_date][period["periodo"]]["wind_gusts"] = {"direction": period["direccion"],
                                                                    "speed": period["velocidad"]}
            except KeyError:
                sections[aux_date]["00-24"]["wind_gusts"] = {"direction": period["direccion"],
                                                                       "speed": period["velocidad"]}
    new_forecast = Forecast(response_dict[0]["nombre"], city_code, True, update_time, sections)
    return new_forecast


def get_code_from_name(city_name):  #This is not the ideal way to get the forecast. I would recommend getting it by code
    response_dict=json.loads(requests.get("https://opendata.aemet.es/opendata/api/maestro/municipios", headers={"api_key" : cfg.api_key}).text)
    search = list(filter(lambda city: city['nombre'] == city_name, response_dict))
    if(len(search)>1):
        raise Warning("More than one match. Returning all matches as list.")
    matches = {}
    for results in search:
        matches[results["nombre"]] = {}
        matches[results["nombre"]]=results["id"].removeprefix("id")  #This was introduced in Python 3.9
    print(matches)
    return matches

class Forecast:
    def __init__(self, city_name, city_code, is_daily, update_time, sections):
        self.city_name = city_name
        self.city_code = city_code
        self.is_daily = is_daily
        self.update_time = update_time
        self.sections = sections

    @classmethod
    def refresh_forecast(self):
        get_forecast_daily_from_code(self.city_code)


