#TODO: creare ts, trovare ritardo ed ultima stazione di ogni treno + cancellato, passare a tommy per gui suca
#Developer: Federico De Rocco
#Dependencies: trainMonitor, viaggiaTreno API

from __future__ import print_function

import sys
import json
import datetime
import time
import trainStatus
import setWindow
from TrainMonitor import viaggiatreno

sW=setWindow
api=viaggiatreno.API()

def is_valid_timestamp(ts):
    return (ts is not None) and (ts > 0) and (ts < 2147483648000)
    
def format_timestamp(ts, fmt='%Y-%m-%dT%H:%M:%S'):
    if is_valid_timestamp(ts):
        return datetime.datetime.fromtimestamp(ts).strftime(fmt)
    else:
        return 'N/A'
    
def formatTimestampClock(ts, fmt='%H:%M'):
    if is_valid_timestamp(ts):
        return datetime.datetime.fromtimestamp(ts/1000).strftime(fmt)
    else:
        return 'N/A'
    
def getTreni(stA, stB, ts, n):
    allTrains = api.call("soluzioniViaggioNew", stA, stB, ts)
    allTrains=json.loads(allTrains)
    treni=[]
    n=min(n, len(allTrains["soluzioni"]))
    for n in range(n):
        treni.append(allTrains["soluzioni"][n]["vehicles"][0]["numeroTreno"])
    return treni  

def getFilteredList(stA, stB, n):
    api=viaggiatreno.API()    
    ts=format_timestamp(time.time()-900)#get timestamp of 15 minutes ago
    treni=getTreni(stA, stB, ts, n)#find the first 15 trains on this track
    treniOrario=trainStatus.checkTrainList(treni, "S01640")
    treniOrario=trainStatus.filterTrainList(treniOrario, time.time()) 
    return treniOrario  

def setRow(rowLayout, train):
    trainWidget=[]
    trainWidget.append(sW.QLabel(train["trainID"]))
    if "error" in train:
        trainWidget.append(sW.QLabel(train["error"]))
        trainWidget.append(sW.QLabel("--"))
        if train["error"]=="Not departed":
            trainWidget.append(sW.QLabel(formatTimestampClock(train["expectedStation"])))
        else:
            trainWidget.append(sW.QLabel("--"))
        
    else:
        trainWidget.append(sW.QLabel(train["lastStation"]))
        trainWidget.append(sW.QLabel(formatTimestampClock(train["lastTime"])))
        trainWidget.append(sW.QLabel(formatTimestampClock(train["expectedStation"])))
    
    for x in trainWidget:
        trainWidget.setAlignment(sW.Qt.AlignmentFlag.AlignCenter)
        
    for x in trainWidget:
        rowLayout.addWidget(x)
        
    return
    
    
	

if __name__ == '__main__':
    
    trains=getFilteredList(1640, 1039, 5)
    
    
    sW.rows
    
    #ciaoTommaso
	
        
    
    
