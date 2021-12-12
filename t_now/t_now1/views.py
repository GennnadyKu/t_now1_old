import numpy as np
import pandas as pd
from io import StringIO
import requests
from django.shortcuts import render
import datetime

# Create your views here.

def tempth():
    # читаем температуру с первого канала 2 последних значений
    # возвращаеm последнее
    #response2 = requests.get("https://api.thingspeak.com/channels/1283823/fields/1.csv?results=2")
    response2 = requests.get("https://api.thingspeak.com/channels/1283823/fields/1.csv?results=2&timezone=Europe/Kiev")
    TESTDATA = StringIO(response2.text)
    data_6 = pd.read_csv(TESTDATA, sep=",")
    #print(data_6)

    data_6n = data_6.to_numpy() # v massiv numpy

    row = 0
    temp1mass = np.zeros((1))
    
    for i in range(len(data_6)):
        if (data_6n[i,2] < 0) or (data_6n[i,2] >0) :
            temp1mass[row] = data_6n[i,2]
            ret_spis = {data_6n[i,0]: temp1mass[row]}
            row = row+1
            #print(temp1mass)
            
    #print(ret_spis)
    return(ret_spis)        



def index(request):
    now = datetime.datetime.now()
    date_time = now.strftime("%d-%m-%Y, %H:%M:%S")
    temp1 = tempth()  
    time_read = list(temp1.keys())[0]
    tmr = time_read.split()[1]
    return render(request, "t_now1/index.html", {
        "newyear": now.month == 12 and now.day ==31,
        #"temp_to":temp1,
        #"time_to": next(iter(temp1)),
        "time_to": tmr,
        #"time_to": list(temp1.keys())[0],
        "temp_to": list(temp1.values())[0],
        "day_to":date_time
    })

