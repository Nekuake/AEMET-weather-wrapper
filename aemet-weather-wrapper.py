import requests
import pprint
import weather_config as cfg



def config(new_api_key):
	if (check_connection(new_api_key)):
		weather_config.api_key=new_api_key

def config():
	new_api_key=input("Paste API Key. You can get it from https://opendata.aemet.es/centrodedescargas/altaUsuario>>")
	if (check_connection(new_api_key)):
		weather_config.api_key=new_api_key

def check_connection(api_key):
	if api_key == "":
		return false #We would just check if server returns a 200 or a 401 but as for 15/03/22 if the api_key is blank, it will just return an empty 200.
	else:
		r = requests.get('https://opendata.aemet.es/opendata/api/maestro/municipios', headers={"api_key":api_key)
		if r.status_code == "200":
			print ("API Key and connection OK")
			return true
		else:
			print ("Request returned "+ r.status_code)
			return false

def external_help():  #Downloads and shows AEMET's OpenData JSON
	r=requests.get("https://opendata.aemet.es/AEMET_OpenData_specification.json", headers={"api_key":api_key})
	



class Forecast:
	def __init__(city_name, city_code, days[]):
		self.city_name=city_name
		self.city_code=city_code
		self.days=days
	)

	@classmethod
	def refresh_forecast(api_key):
		

