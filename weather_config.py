# Add the key for the OpenData API. Please note that this file is included in the gitignore but double-check whenever
# you share, push or work with these files.

api_key = ""
"""
Translating AEMET's status_weather_codes to something more readable, with description. It will be a big dictionary
but I hope it's more useful. Descriptions are based on https://www.aemet.es/es/eltiempo/prediccion/espana/ayuda.
You can get the AEMET's values scrapping all the pngs contained in https://www.aemet.es/imagenes/png/estado_cielo/
i.e.:
for x in range(0,99):
    r = requests.get("https://www.aemet.es/imagenes/png/estado_cielo/" + str(x) +".png", stream=True)
    if r.status_code == 200:
        with open(str(x)+".png", 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)
My approach for the values divides the tens and units this way:

#################################################################
                        Tens        Units
    no rain	                1	    1	    cloudy intervals
    light rain	            2	    2	    cloudy
    rain	                3	    3	    very cloudy
    light snowfall	        4	    4	    overcast
    snowfall	            5		
    storm	                6		
    storm with light rain   7		
#################################################################
Special:
    sunny               1
    little cloudy       2
    high clouds         10
    fog                 97
    mist                98
    haze                99
#################################################################
With these simple rules you can get combined values like "

"""
# How values are made
status_weather_codes = {
    "11": {"value": 1,
           "description": "sunny"},
    "12": {"value": 2,
           "description": "little cloudy"},
    "13": {"value": 11,
           "description": "cloudy intervals"},
    "14": {"value": 12,
           "description": "cloudy"},
    "15": {"value": 13,
           "description": "very cloudy"},
    "16": {"value": 14,
           "description": "overcast"},
    "17": {"value": 10,
           "description": "high clouds"},
    "23": {"value": 31,
           "description": "cloudy intervals with rain"},
    "24": {"value": 32,
           "description": "cloudy with rain"},
    "25": {"value": 33,
           "description": "very cloudy rain"},
    "26": {"value": 34,
           "description": "overcast rain"},
    "27": {"value": 31,  # This one is repeated in their codes.
           "description": "cloudy intervals with rain"},
    "33": {"value": 51,
           "description": "cloudy intervals with snowfall"},
    "34": {"value": 52,
           "description": "cloudy with snowfall"},
    "35": {"value": 53,
           "description": "very cloudy intervals with snowfall"},
    "36": {"value": 54,
           "description": "overcast with snowfall"},
    "43": {"value": 21,
           "description": "cloudy intervals with light rain"},
    "44": {"value": 22,
           "description": "cloudy with ligh rain"},
    "45": {"value": 23,
           "description": "very cloudy with light rain"},
    "46": {"value": 24,
           "description": "overcast with light rain"},
    "51": {"value": 61,
           "description": "cloudy intervals with storm"},
    "52": {"value": 62,
           "description": "cloudy with storm"},
    "53": {"value": 63,
           "description": "very cloudy intervals with storm"},
    "54": {"value": 64,
           "description": "overcast with storm"},
    "61": {"value": 71,
           "description": "cloudy intervals with light rain and storm"},
    "62": {"value": 72,
           "description": "cloudy with light rain and storm"},
    "63": {"value": 73,
           "description": "very cloudy with light rain and storm"},
    "64": {"value": 74,
           "description": "overcast with light rain and storm"},
    "71": {"value": 41,
           "description": "cloudy intervals with light snowfall"},
    "72": {"value": 42,
           "description": "cloudy with light snowfall"},
    "73": {"value": 43,
           "description": "very cloudy intervals with light snowfall"},
    "74": {"value": 44,
           "description": "overcast with light snowfall"},
    "81": {"value": 97,
           "description": "fog"},
    "82": {"value": 98,
           "description": "mist"},
    "83": {"value": 99,
           "description": "haze"},
}
