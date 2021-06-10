# -*- coding: utf-8 -*-
"""
Created on Fri Jul 10 14:34:31 2020

@author: spal0
"""

#!/usr/bin/env python
# coding: utf-8

# In[1]:
class data:
    value =[]
    time =[]

class datas:
    heart=[]
    time=[]
    

#import chardet
#import urllib3
#import netifaces
import pandas as pd
from scipy.signal import butter, lfilter
from datetime import datetime
import matplotlib.pyplot as plt
from scipy.signal import hilbert, chirp

import math
#from scipy import signal
#from datetime import datetime, date
from influxdb import InfluxDBClient
#from operator import attrgetter
import numpy
##import subprocess
#import random
#import time
import operator
#import ConfigParser
##import sys
#import logging
from detect_peaks import detect_peaks
#from scipy.stats import kurtosis 
#from scipy import stats 
#import nitime.algorithms as nt_alg
#import nitime.utils as nt_ut
import numpy as np
from numpy import array
#import scipy as sp
#import threading
#from datetime import datetime
#from dateutil import tz
#import pytz
#import smtplib
#import ast
import statsmodels.api as sm
#import netifaces
##import json
#import requests


# In[2]:


def butter_lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a

def butter_lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = lfilter(b, a, data)
    return y


# In[5]:


def calculateBP_v2(signal, fs, cutoff,nlags,order):
    
    signalFiltered = butter_lowpass_filter(signal, cutoff, fs, order)
    print(signalFiltered[0])
    
    arrSignal = array( signalFiltered )
    auto = sm.tsa.stattools.acf(arrSignal, unbiased=False, nlags=nlags,qstat=False)
    peaks = detect_peaks(auto,show=False)
    
    bp1=(976.35,0,0,427.48,0,-1148.9,-2094.9,535.67)
    bp11=(0,0,0,0,0,1503.6)
    bp12=(0,0,0,0,-488.87)
    bp13=(0,0,0,0)
    bp14=(0,0,-100.64)
    bp15=(2657.5,-1182.4)
    bp16=(206.17)
    
    bp2=(-31.933,0,0,-912.89,0,-11870,8201.5,2095.8)
    bp21=(0,0,0,0,0,-6.9995)
    bp22=(0,0,0,0,676.65)
    bp23=(0,0,0,0)
    bp24=(0,0,1130.8)
    bp25=(3801.5,8920.9)
    bp26=(-11246)
    #print(peaks)
    bptt1 = peaks[0:7]/fs
    #print(bptt1)
    bptt11 = bptt1[0]*bptt1[1:7]
    bptt12 = bptt1[1]*bptt1[2:7]
    bptt13 = bptt1[2]*bptt1[3:7]
    bptt14 = bptt1[3]*bptt1[4:7]
    bptt15 = bptt1[4]*bptt1[5:7]
    bptt16 = bptt1[5]*bptt1[6:7]
    #print(bptt1[5])
    
    bpttlow = bp1[1:8]
    bptthigh = bp2[1:8]
    
    bplow =np.ceil(np.absolute(np.dot(bptt1,bpttlow)+np.dot(bptt11,bp11)+np.dot(bptt12,bp12)+np.dot(bptt13,bp13)+np.dot(bptt14,bp14)+np.dot(bptt15,bp15)+np.dot(bptt16,bp16)+bp1[0]))
    bphigh=np.ceil(np.absolute(np.dot(bptt1,bptthigh)+np.dot(bptt11,bp21)+np.dot(bptt12,bp22)+np.dot(bptt13,bp23)+np.dot(bptt14,bp24)+np.dot(bptt15,bp25)+np.dot(bptt16,bp26)+bp2[0]))
    
    
    return bplow,bphigh


# In[9]:


# demo
client = InfluxDBClient("18.222.223.195", "8086", "Jose", "sensorweb", "shake")
unit = "b8:27:eb:8d:ae:69"

dataset = pd.read_csv("data(both).csv")

#print(dataset)
##yajie
#stampIni = "2020-02-03T19:03:30.000Z"
#stampEnd = "2020-02-03T19:07:30.000Z"

##Fangyu
stampIni = "2020-02-03T19:22:15.000Z";
stampEnd = "2020-02-03T19:27:15.000Z";

query = 'SELECT "value" FROM Z WHERE ("location" = \''+unit+'\')  and time >= \''+stampIni+'\' and time <= \''+stampEnd+'\'   '

result = client.query(query)
points = list(result.get_points())

values =  map(operator.itemgetter('value'), points)
times  =  map(operator.itemgetter('time'),  points)
#print(values)
#data.value =  map(operator.itemgetter('value'), points)
#data.time  =  map(operator.itemgetter('time'),  points)

#data.value = list(dataset.heart)
datas.heart = list(values)
datas.time = list(times)

#print(data.value[0])
#print(datas.time)
a_string = datas.time[11].replace("2020-02-03T", "")
a_string = a_string.replace("Z", "")
#print(a_string)
timeobj = datetime.strptime(a_string, "%H:%M:%S.%f")
#print(timeobj)
#print(size(timeobj))
#print(type(timeobj))
#print(timeobj)
mytime = "2015-02-16 10:36:41.387000"
myTime = datetime.strptime(mytime, "%Y-%m-%d %H:%M:%S.%f")
#print(mytime)
#print(timeobj-myTime)
#print(dataset.heart)
##

cutoff = 4
fs = 100
order = 1
nlags = 250
hrw =0.75
print(dataset.heart[0:10])
bplow, bphigh = calculateBP_v2(dataset.heart, fs, cutoff,nlags,order)
print(dataset.heart[0:10])
print(bplow)
print(bphigh)

#dataset=pd.DataFrame(datas.heart, columns =['heart'])
#print(dataset['heart'])
#dataset=pd.DataFrame(datas.time, columns =['time'])
#dataset.keys=['heart','time']
#print(dataset.keys)

#print(dataset)

mov_avg = dataset['heart'].rolling(int(hrw*fs)).mean() #Calculate moving average
#Impute where moving average function returns NaN, which is the beginning of the signal where x hrw
avg_hr = (np.mean(dataset.heart))
#print(mov_avg)
mov_avg = [avg_hr if math.isnan(x) else x for x in mov_avg]
#print(mov_avg)
mov_avg = [x*1.2 for x in mov_avg] #For now we raise the average by 20% to prevent the secondary heart contraction from interfering, in part 2 we will do this dynamically
#print(mov_avg)
dataset['heart_rollingmean'] = mov_avg #Append the moving average to the dataframe

#Mark regions of interest
window = []
peaklist = []
peaktime =[]
listpos = 0 #We use a counter to move over the different data columns
i=0
for datapoint in dataset.heart:
    rollingmean = dataset.heart_rollingmean[listpos] #Get local mean
    if (datapoint < rollingmean) and (len(window) < 1): #If no detectable R-complex activity -> do nothing
        listpos += 1
    elif (datapoint > rollingmean): #If signal comes above local mean, mark ROI
        window.append(datapoint)
        listpos += 1
    else: #If signal drops below local mean -> determine highest point
        maximum = max(window)
        i+=1
        beatposition = listpos - len(window) + (window.index(max(window))) #Notate the position of the point on the X-axis
        peaklist.append(beatposition) #Add detected peak to list
        #peaktime.append(dataset.time[listpos])
        #if i==3:
         #   timeobj = datetime.strptime(dataset.time[listpos], '%H:%M:%S')
        #if i==150:
         #   timeobj2 = datetime.strptime(dataset.time[listpos], '%H:%M:%S')
        window = [] #Clear marked ROI
        listpos += 1
print("Done")
listpos=0
i=0
window1=[]
peaklist1=[]
#print(dataset.heart)
print("Done again")
ybeat = [dataset.heart[x] for x in peaklist] #Get the y-value of all peaks for plotting purposes#
ybeat1 = [dataset.heart[x] for x in peaklist1] #Get the y-value of all peaks for plotting purposes#
RR_list = []
cnt = 0
plt.title("Detected peaks in signal")
plt.xlim(2000,5000)
plt.ylim(-50000,50000)
plt.plot(dataset.heart, alpha=0.5, color='blue', label="Signal after BPF") #Plot semi-transparent HR
plt.plot(mov_avg, color ='green', label="moving average") #Plot moving average
plt.scatter(peaklist, ybeat, color='red') #, label="average: %.1f BPM" %bpm) #Plot detected peaks
plt.scatter(peaklist1, ybeat1, color='blue')
#plt.plot(amplitude_envelope, color='red', label='amp')
plt.legend(loc=4, framealpha=0.6)
plt.show()

#sos = signal.butter(10, 0.7, 8, 'bp', fs=100, output='sos')
#filtered = signal.sosfilt(sos, dataset)
#plt.plot(filtered)
#plt.show()