from scipy.interpolate import interp1d
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline
import pandas as pd
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
import matplotlib.dates as mdates
import datetime
from scipy import integrate

pannello=pd.read_csv("pannello.csv" ,sep=' ',parse_dates=['timestamp'], index_col='timestamp')
pannello.index = pd.to_datetime(pannello.index, unit='s')
pannello=pannello[pannello['value'] >=0]
pannello=pannello.resample('2T').pad().dropna()
pannello=pannello[0:720]
ore=mdates.date2num(pannello.index)
ore=(ore-ore[0])*86400
campioni=pannello.value
ottimizzazione=[]
indiciOtt=[]
counter=-5 # lavora per 10 minuti ogni 30, salvo pannello dove si attiva dopo soli 10
for i in range(0,len(ore)):
 indiciOtt.append(ore[i])
 if(campioni[i]>0 and counter<=-5 or counter==-15):
  ottimizzazione.append(70)
  counter=1
 elif(counter>0 and counter<5):
  ottimizzazione.append(70-70*counter*0.02)
  counter+=1
 else:
  if(counter>0):
   counter=-1
  else: counter-=1
  ottimizzazione.append(0)

integrazione1=[]
integrazione2=[]
integrazione1.append(0)
integrazione2.append(0)
for i in range(0,len(ore)-1):
  integrazione1.append(integrazione1[-1]+ottimizzazione[i]*120/3600000)
  integrazione2.append(integrazione2[-1]+campioni[i]*120/3600000)
for i in range(len(integrazione1)):
    integrazione1[i] = np.around(integrazione1[i],3)
    integrazione2[i] = np.around(integrazione2[i],3)
plt.plot(indiciOtt,ottimizzazione,indiciOtt,campioni,marker='o')
plt.show()
plt.plot(indiciOtt,integrazione1,indiciOtt,integrazione2)
plt.show()
