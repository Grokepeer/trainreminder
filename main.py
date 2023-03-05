#TODO: creare ts, trovare ritardo ed ultima stazione di ogni treno + cancellato, passare a tommy per gui suca
#Developer: Federico De Rocco
#Dependencies: trainMonitor, viaggiaTreno API

from __future__ import print_function

import sys
import json
import datetime
import time
import trainStatus
from TrainMonitor import viaggiatreno

def is_valid_timestamp(ts):
    return (ts is not None) and (ts > 0) and (ts < 2147483648000)
    
def format_timestamp(ts, fmt='%Y-%m-%dT%H:%M:%S'):
    if is_valid_timestamp(ts):
        return datetime.datetime.fromtimestamp(ts).strftime(fmt)
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
	

if __name__ == '__main__':
    api=viaggiatreno.API()    
    ts=format_timestamp(time.time()-900)#get timestamp of 15 minutes ago
    treni=getTreni(1640, 1039, ts, 5)#find the first 15 trains on this track
    treniOrario=trainStatus.checkTrainList(treni, "S01640")
    treniOrario=trainStatus.filterTrainList(treniOrario, time.time())
    for x in treniOrario:
        print(x)
    #ciaoTommaso
	
        
    
    
