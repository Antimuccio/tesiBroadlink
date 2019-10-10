from scipy.interpolate import interp1d
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline
import pandas as pd
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
import matplotlib.dates as mdates
import datetime

originale=pd.read_csv("75.csv" ,sep = ",",dayfirst=True,parse_dates=['data'], index_col='data')
confronto=pd.read_csv("47.csv" ,sep = ",",dayfirst=True,parse_dates=['data'], index_col='data')
confronto=confronto.resample('1T').pad() #compensa campioni mancanti
fmin=[]
fmax =[]
minI=[]
maxI=[]
ore=mdates.date2num(originale.index)
ore=(ore-ore[0])*86400
campioni=originale.value-originale.value[0]
confrontov=confronto.value-confronto.value[0]
indici=mdates.date2num(confronto.index)
indici=(indici-indici[0])*86400
for i in range(1,ore.size-1):
    if campioni[i]>campioni[i-1] and campioni[i]-campioni[i+1]<0.0025:
        fmax.append(campioni[i])
        maxI.append(ore[i])
    if campioni[i]<campioni[i+1] and campioni[i]-campioni[i-1]<0.0025:
        fmin.append(campioni[i])
        minI.append(ore[i])

csMax=CubicSpline(maxI, fmax,bc_type='clamped')
csMin=CubicSpline(minI, fmin,bc_type='clamped')
x=np.linspace(ore[0],ore[-1], len(ore))
plt.suptitle('Energia')
plt.plot(x,confrontov,label='altro',color='magenta')
ottimizzazione=[]
ottimizzazione.append(x[0])
ottI=[]
ottI.append(0)
for i in range(1,len(x)):
 ottI.append(x[i])
 if ottimizzazione[i-1]<=(csMax(x[i])-(csMax(x[i])-csMin(x[i]))) and confrontov[i]==confrontov[i-1] :
    ottimizzazione.append(campioni[i])
 else:
    if ottimizzazione[i-1]>csMin(x[i]):
     ottimizzazione.append(ottimizzazione[i-1])
    else:
     print(0.05*(x[i]-x[i-1])/3600)
     ottimizzazione.append(ottimizzazione[i-1]+0.05*(x[i]-x[i-1])/3600)
plt.plot(ore,campioni,color='black',label='originale',linestyle='--')
plt.plot(ottI,ottimizzazione,label='curvaGenerata')
plt.plot(x,csMax(x),label='fmax',linestyle=':',color='orange')
plt.plot(x,csMin(x),label='fmin',linestyle=':',color='green')
plt.xlabel('secondi')
plt.ylabel('kWh')
plt.legend()
plt.show()
