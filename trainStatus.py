#Developers: Federico De Rocco, Tommaso Bertelli

from __future__ import print_function

import sys
import datetime
import json
from TrainMonitor import viaggiatreno

api=viaggiatreno.API()


def getTrainStatus(trainID):
	departures = api.call("cercaNumeroTrenoTrenoAutocomplete", trainID)
	return api.call("andamentoTreno", departures[0][1], trainID, departures[0][2])

def checkTrain(trainID, stationFullID):
	apiReport=getTrainStatus(trainID)
	trainTime=dict()
	trainTime["trainID"]=trainID

	if apiReport['tipoTreno'] == 'ST' or apiReport['provvedimento'] == 1: #train is cancelled
		trainTime["error"]="Cancelled"

	if apiReport["oraUltimoRilevamento"] == None:	#train is not departed yet
		trainTime["error"]="Not departed"

	
	for i in range(len(apiReport["fermate"])): #gets position of the station in the list
		if apiReport["fermate"][i]["id"] == stationFullID:
			break

	trainTime["lastStation"]=apiReport["stazioneUltimoRilevamento"]
	trainTime["tsLastStation"]=apiReport["oraUltimoRilevamento"]
	trainTime["delay"]=apiReport["ritardo"]
	trainTime["expectedStation"]=apiReport["fermate"][i]["partenza_teorica"]

	return trainTime
	
def checkTrainList(trains, stationFullID):
	listTrainTime=[]
	for x in trains:
		listTrainTime.append(checkTrain(x, stationFullID))
	return listTrainTime

def filterTrainList(trains, ts):
	for x in trains:
		if x["expectedStation"] != None:
			if x["expectedStation"]<ts:
				trains.remove(x)
	return trains
