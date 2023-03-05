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
        station=train["lastStation"].removeprefix("MILANO ")
        if len(station)>12:
            station = station[:-(len(station)-12)]
            station= station.rstrip(" .")
            station=station+"."
        trainWidget.append(sW.QLabel(station))
        trainWidget.append(sW.QLabel(formatTimestampClock(train["tsLastStation"])))
        trainWidget.append(sW.QLabel(formatTimestampClock(train["expectedStation"])))
    
    for x in trainWidget:
        x.setAlignment(sW.Qt.AlignmentFlag.AlignCenter)
        
    for x in trainWidget:
        rowLayout.addWidget(x)
        
    return

def setRowsWindow(trains, rows, rowsLayout):
    trainID=sW.QLabel("Train ID")
    trainID.setAlignment(sW.Qt.AlignmentFlag.AlignCenter)
    rowsLayout[0].addWidget(trainID)
    
    LastIn=sW.QLabel("LastTracking")
    LastIn.setAlignment(sW.Qt.AlignmentFlag.AlignCenter)
    rowsLayout[0].addWidget(LastIn)
    
    LastAt=sW.QLabel("Last At")
    LastAt.setAlignment(sW.Qt.AlignmentFlag.AlignCenter)
    rowsLayout[0].addWidget(LastAt)
    
    departures=sW.QLabel("Expected")
    departures.setAlignment(sW.Qt.AlignmentFlag.AlignCenter)
    rowsLayout[0].addWidget(departures)
    
    n=min(len(rowsLayout)-1, len(trains))
    for x in range(0,n):
        setRow(rowsLayout[x+1], trains[x])
    sW.assignLayoutRows(rows, rowsLayout)
    
    return

if __name__ == '__main__':
    
    trains=getFilteredList(1039, 1640, 5)
    setRowsWindow(trains, sW.rows, sW.rowsLayout)
    layoutWindow=sW.QVBoxLayout()
    
    for x in sW.rows:
        layoutWindow.addWidget(x)
    
    widget=sW.QWidget()
    widget.setLayout(layoutWindow)
    sW.window.setCentralWidget(widget)
    sW.app.exec()
    #ciaoTommaso
	
        
    
    
