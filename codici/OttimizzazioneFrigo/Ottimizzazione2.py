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

originale=pd.read_csv("74.csv" ,sep = ",",dayfirst=True,parse_dates=['data'], index_col='data')
confronto = pd.read_csv('frigo.csv',sep=' ',parse_dates=['timestamp'], index_col='timestamp')
confronto.index = pd.to_datetime(confronto.index, unit='s')
confronto=confronto[confronto['value'] < 400]
confronto=confronto[confronto['value'] >=0]
confronto=confronto.resample('2T').pad().dropna()
ore=mdates.date2num(originale.index)
ore=(ore-ore[0])*86400
confrontov=confronto.loc[confronto.index].values
campioni=originale.loc[originale.index].values
ottimizzazione=[]
indiciOtt=[]
picco=None
seguiO=False
for i in range(0,len(ore)):
 indiciOtt.append(ore[i])
 if campioni[i]-campioni[i-1]<-30 and seguiO:
  ottimizzazione.append(campioni[i-1])
  seguiO=False
 else:
  if (confrontov[i]>30 and campioni[i]-campioni[i-1]>20):
      if picco is  None:
       picco=campioni[i]
      else:
       picco=max(picco,campioni[i])
      ottimizzazione.append(0)
      seguiO=True
  else :
   if(picco is not None):
    ottimizzazione.append(picco)
    picco=None
   else:
    ottimizzazione.append(campioni[i])
integrazione1=[]
integrazione2=[]
integrazione1.append(0)
integrazione2.append(0)
print("primocaso",np.nanmax(confrontov[0:len(campioni)]+campioni))
print("secondocaso",np.nanmax(confrontov[0:len(ottimizzazione)]+ottimizzazione))
for i in range(1,len(ore)):
  integrazione1.append(integrazione1[-1]+ottimizzazione[i]*120/3600000)
  integrazione2.append(integrazione2[-1]+campioni[i]*120/3600000)
for i in range(len(integrazione1)):
    integrazione1[i] = np.around(integrazione1[i],2)
    integrazione2[i] = np.around(integrazione2[i],2)
fmin=[]
fmax =[]
minI=[]
maxI=[]
for i in range(0,ore.size-2):
    if integrazione2[i+1]-integrazione2[i]>=0.008 and integrazione2[i+2]-integrazione2[i+1]==0 :
        fmax.append(integrazione2[i+1])
        maxI.append(ore[i+1])
        fmin.append(integrazione2[i])
        minI.append(ore[i])
csMax=CubicSpline(maxI,fmax,bc_type='natural')
csMin=CubicSpline(minI,fmin,bc_type='natural')
x=np.linspace(ore[0],ore[-1], 2*ore.size)
plt.suptitle('Energia')
ax1=plt.subplot(211)
ax2=plt.subplot(212)
ax1.plot(ore,campioni,color='black',label='originale',linestyle='--',marker='o')
ax1.plot(ore,confrontov[0:len(originale)],label='altro',color='magenta')
ax1.plot(indiciOtt,ottimizzazione)
ax1.set_xlabel('secondi')
ax1.set_ylabel('W')
ax2.plot(x,csMax(x),x,csMin(x),x,csMax(x)+csMax(x)*0.05,x,csMin(x)-csMin(x)*0.05)
ax2.plot(ore,integrazione1,ore,integrazione2)
plt.show()
