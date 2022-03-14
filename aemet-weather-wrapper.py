import requests


global api_key=null


def config(new_api_key):
	api_key=new_api_key

def external_help():  #Downloads and shows AEMET's OpenData JSON
	r=requests.get(https://opendata.aemet.es/AEMET_OpenData_specification.json)
	



class Forecast:
	def __init__(city_name, city_code, days[]):
		self.city_name=city_name
		self.city_code=city_code
		self.days=days
	)

	@classmethod
	def refresh_forecast(api_key):
		

