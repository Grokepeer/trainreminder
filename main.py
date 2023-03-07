#TODO: add statusBar
#Developer: Federico De Rocco
#Dependencies: trainMonitor, viaggiaTreno API

from __future__ import print_function

import json
import datetime
from threading import Timer
import time
import trainStatus
import setWindow
from TrainMonitor import viaggiatreno

sW=setWindow
api=viaggiatreno.API()
jsonFile=open("settings.json")
settings=json.load(jsonFile)
jsonFile.close()
trains=[]

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
        trainWidget.append(sW.QLabel("--"))

        
    else:
        station=train["lastStation"].removeprefix("MILANO ")
        if len(station)>10:
            station = station[:-(len(station)-10)]
            if station[len(station)-1]==" ":
                station= station.rstrip(" ")
            else:
                if station[len(station)-1]!=".":
                    station=station+"."
        trainWidget.append(sW.QLabel(station))
        trainWidget.append(sW.QLabel(formatTimestampClock(train["tsLastStation"])))
        trainWidget.append(sW.QLabel(formatTimestampClock(train["expectedStation"])))
        trainWidget.append(sW.QLabel(str(train["delay"])))

    for x in trainWidget:
        x.setAlignment(sW.Qt.AlignmentFlag.AlignCenter)
        
    for x in trainWidget:
        rowLayout.addWidget(x)
        
    return

def setRowsWindow(trains, rows, rowsLayout):
    trainID=sW.QLabel("ID")
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
    
    departures=sW.QLabel("Delay")
    departures.setAlignment(sW.Qt.AlignmentFlag.AlignCenter)
    rowsLayout[0].addWidget(departures)
    
    n=min(len(rowsLayout)-1, len(trains))
    for x in range(0,n):
        setRow(rowsLayout[x+1], trains[x])
    sW.assignLayoutRows(rows, rowsLayout)
    
    return

def refreshWindow(settings):
    trains=getFilteredList(settings["departuresStationID"], settings["arrivalStationID"], 6)
    refreshWindowSettings(settings, trains)
    sW.trainMonitor.setTrains(trains)
    return

def refreshWindowSettings(settings, trains):
    sW.rows=sW.initRows(6)
    sW.rowsLayout=sW.initRowsLayout(6)
    setRowsWindow(trains, sW.rows, sW.rowsLayout)
    layoutWindow=sW.QVBoxLayout()
    

    for x in sW.rows:
        layoutWindow.addWidget(x)

    sW.trainMonitor.setNewLayout(layoutWindow)
    return

def resetSettings():
    sW.trainSettings=sW.settingsWindow()
    return
        

if __name__ == '__main__':
    trainStatus.delayMargin=settings["delayMargin"]
    trainStatus.delaySafe=settings["delaySafe"]
    sW.app.setFont(sW.QFont("Fira Code", settings["fontPts"]))
    

    trains=getFilteredList(settings["departuresStationID"], settings["arrivalStationID"], 6)
    setRowsWindow(trains, sW.rows, sW.rowsLayout)
    layoutWindow=sW.QVBoxLayout()
    
    sW.trainMonitor.setTrains(trains)

    
    for x in sW.rows:
        layoutWindow.addWidget(x)
    
    widget=sW.QWidget()
    widget.setLayout(layoutWindow)
    sW.trainMonitor.setCentralWidget(widget)
    
    
    sW.app.exec()
    
    
    #ciaoTommaso
	
        
    
    
