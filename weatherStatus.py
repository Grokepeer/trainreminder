import requests


class weatherAPI:
	def __init__(self, options):
		self.latitude=options["latitude"]
		self.longitude=options["longitude"]
		self.url="https://api.open-meteo.com/v1/forecast?"
		self.url=self.url+"latitude="+str(self.latitude)+"&longitude="+str(self.longitude)
		self.url=self.url+"&daily=temperature_2m_max,temperature_2m_min,apparent_temperature_max,apparent_temperature_min,precipitation_sum,precipitation_probability_max,windspeed_10m_max&timeformat=unixtime&forecast_days=1&timezone=Europe%2FBerlin"
		return

	def callAPI(self):
		response=requests.get(self.url)
		return response.json()
	
	def changeOptions(self, options):
		self.latitude=options["latuitude"]
		self.longitude=options["longitude"]
		self.url="https://api.open-meteo.com/v1/forecast?"
		url=url+"latitude"+str(self.latitude)+"&longitude="+str(self.longitude)
		url=url+"&daily=temperature_2m_max,temperature_2m_min,apparent_temperature_max,apparent_temperature_min,precipitation_sum,precipitation_probability_max,windspeed_10m_max&timeformat=unixtime&forecast_days=1&timezone=Europe%2FBerlin"
		return

	def callFiltered(self, options):
		response=self.callAPI()
		data=dict()
		if "error" in response:
			return 1

		data["temperatureMax"]=response["daily"]["temperature_2m_max"][0]
		data["temperatureMin"]=response["daily"]["temperature_2m_min"][0]
		data["apparentTemperatureMax"]=response["daily"]["apparent_temperature_max"][0]
		data["apparentTemperatureMin"]=response["daily"]["apparent_temperature_min"][0]
		data["precipitation"]=response["daily"]["precipitation_sum"][0]
		data["precipitationProbability"]=response["daily"]["precipitation_probability_max"][0]
		data["windspeedMax"]=response["daily"]["windspeed_10m_max"][0]
		return data