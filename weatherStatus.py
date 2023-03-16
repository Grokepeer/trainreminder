import requests


class weatherAPI:
	def __init__(self, options):
		self.latitude=options["latitude"]
		self.longitude=options["longitude"]
		self.url="https://api.open-meteo.com/v1/forecast?"
		url=url+"latitude"+self.latitude+"&longitude="+self.longitude
		url=url+"&daily=temperature_2m_max,temperature_2m_min,apparent_temperature_max,apparent_temperature_min,precipitation_sum,precipitation_probability_max,windspeed_10m_max&timeformat=unixtime&forecast_days=1&timezone=Europe%2FBerlin"
		return

	def callAPI(self):
		response=requests.get(self.url)
		return response.json()
	
	def changeOptions(self, options):
		self.latitude=options["latuitude"]
		self.longitude=options["longitude"]
		self.url="https://api.open-meteo.com/v1/forecast?"
		url=url+"latitude"+self.latitude+"&longitude="+self.longitude
		url=url+"&daily=temperature_2m_max,temperature_2m_min,apparent_temperature_max,apparent_temperature_min,precipitation_sum,precipitation_probability_max,windspeed_10m_max&timeformat=unixtime&forecast_days=1&timezone=Europe%2FBerlin"
		return

	def callFiltered(self):
		response=self.callAPI()
		data=dict()
		data["temperatureMax"]=response["temperature_2m_max"]
		data["temperatureMin"]=response["temperature_2m_min"]
		data["apparentTemperatureMax"]=response["apparent_temperature_max"]
		data["apparentTemperatureMin"]=response["apparent_temperature_min"]
		data["precipitation"]=response["precipitation_sum"]
		data["precipitationProbability"]=response["precipitationProbability"]
		data["windspeedMax"]=response["windspeed_10m_max"]
		return data