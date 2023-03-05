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
		return trainTime
	if apiReport["oraUltimoRilevamento"] == None:	#train is not departed yet
		trainTime["error"]="Not departed"
		return trainTime
	
	for i in range(len(apiReport["fermate"])): #get position of the station in the list
		if apiReport["fermate"][i]["id"] == stationFullID:
			break

	trainTime["lastStation"]=apiReport["stazioneUltimoRilevamento"]
	trainTime["tsLastStation"]=apiReport["oraUltimoRilevamento"]
	trainTime["delay"]=apiReport["ritardo"]
	trainTime["expectedCertosa"]=apiReport["fermate"][i]["partenza_teorica"]

	return trainTime
	

def checkTrainList(trains, stationFullID):
	listTrainTime=[]
	for x in trains:
		listTrainTime.append(checkTrain(x, stationFullID))
	return listTrainTime
