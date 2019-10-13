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
lavatrice =pd.read_csv('lavatrice.csv',sep=' ',parse_dates=['timestamp'], index_col='timestamp')
confronto = pd.read_csv('frigo.csv',sep=' ',parse_dates=['timestamp'], index_col='timestamp')
confronto.index = pd.to_datetime(confronto.index, unit='s')
confronto=confronto[confronto['value'] < 3300]
confronto=confronto[confronto['value'] >=0]
confronto=confronto.resample('2T').pad().dropna()
lavatrice.index = pd.to_datetime(lavatrice.index, unit='s')
lavatrice=lavatrice[lavatrice['value'] < 3300]
lavatrice=lavatrice[lavatrice['value'] >=0]
lavatrice=lavatrice.resample('2T').pad().dropna()
ore=mdates.date2num(originale.index)
ore=(ore-ore[0])*86400
confrontov=np.round(confronto.loc[confronto.index].values,2)
campioni=np.round(originale.loc[originale.index].values,2)
confrontoL=np.round(lavatrice.loc[confronto.index].values,2)
confrontoL=confrontoL[0:len(campioni)]
confrontov=confrontov[0:len(campioni)]
ottimizzazione=[]
indiciOtt=[]
seguiO=False
for i in range(0,len(ore)):
 indiciOtt.append(ore[i])
 if (confrontov[i]+confrontoL[i]>500 and confrontov[i]+confrontoL[i]<confrontov[i+1]+confrontoL[i+1] and campioni[i+1]-campioni[i]>20):
      ottimizzazione.append(campioni[i+1])
      seguiO=True
 elif seguiO:
     if campioni[i+1]-campioni[i]<20 and campioni[i]>20 :
      ottimizzazione.append(campioni[i+1])
     else:
       seguiO=False
       ottimizzazione.append(0)
 else:
    seguiO=False
    ottimizzazione.append(campioni[i])
integrazione1=[]
integrazione2=[]
integrazione1.append(0)
integrazione2.append(0)
numero1=0
indice=0
max1=0
max2=0
max3=0
max4=0
numero2=0
for i in range(0,len(ore)):
 max1=max(confrontov[i]+ottimizzazione[i]+confrontoL[i],max1)
 max2=max(confrontov[i]+campioni[i]+confrontoL[i],max2)
 if(confrontov[i]+ottimizzazione[i]+confrontoL[i]>confrontov[i]+campioni[i]+confrontoL[i]):
   numero1+=1
 if(confrontov[i]+ottimizzazione[i]+confrontoL[i]<confrontov[i]+campioni[i]+confrontoL[i]):
   numero2+=1
print(numero1,numero2,max1,max2)
for i in range(0,len(ore)-1):
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
plt.plot(ore,campioni,color='black',label='originale',linestyle='--',marker='o')
plt.plot(indiciOtt,ottimizzazione,marker='o')
plt.show()
ax1=plt.subplot(211)
ax2=plt.subplot(212)
ax1.plot(ore,campioni,color='black',label='originale',linestyle='--',marker='o')
ax1.plot(ore,confrontov[0:len(originale)],ore,confrontoL[0:len(originale)])
ax1.plot(indiciOtt,ottimizzazione)
ax1.set_xlabel('secondi')
ax1.set_ylabel('W')
ax2.plot(x,csMax(x),x,csMin(x))
ax2.plot(ore,integrazione1,ore,integrazione2)
plt.show()
