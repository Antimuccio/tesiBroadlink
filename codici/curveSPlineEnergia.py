from scipy.interpolate import interp1d
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline
import pandas as pd
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
import matplotlib.dates as mdates

originale=pd.read_csv("75.csv" ,sep = ",",dayfirst=True,parse_dates=['data'], index_col='data')

fmin=[]
fmax =[]
minI=[]
maxI=[]
ore=originale.index
campioni=originale.value
ore=mdates.date2num(ore)
for i in range(1,campioni.size-1):
    if campioni[i]>campioni[i-1] and campioni[i]-campioni[i+1]<0.025:
        fmax.append(campioni[i])
        maxI.append(ore[i])
    if campioni[i]<campioni[i+1] and campioni[i]-campioni[i-1]<0.025:
        fmin.append(campioni[i])
        minI.append(ore[i])



csMax=CubicSpline(maxI, fmax,bc_type='clamped')
csMin=CubicSpline(minI, fmin,bc_type='clamped')
x=np.linspace(ore[0],ore[-1], ore.size)
giorni= mdates.num2date(x)
maxI=mdates.num2date(maxI)
minI=mdates.num2date(minI)
plt.suptitle('Energia')
ax1=plt.subplot(211)
ax2=plt.subplot(212)
ax1.plot(maxI,fmax,label='fmax',marker='o',color='orange')
ax1.plot(minI,fmin,label='fmin',marker='*',color='green')
ax1.plot(ore,campioni,label='originale',color='black')
ax2.plot(ore,campioni,label='originale',color='black')
ax2.plot(giorni,csMax(x),label='fmaxCSP',color='orange')
ax2.plot(giorni,csMin(x),label='fminCSP',color='green')
ax1.set_xlabel('Ora')
ax1.set_ylabel('Consumi')
ax2.set_xlabel('Ora')
ax2.set_ylabel('Consumi')
ax1.legend()
ax2.legend()
plt.show()
minimo=csMax(x[0])-csMin(x[0])
for i in range(1,len(x)):
    if  csMax(x[i])-csMin(x[i])<minimo:
        minimo=csMax(x[i])-csMin(x[i])
a0 = csMax.c.item(3,49)
b0 = csMax.c.item(2,49)
c0 = csMax.c.item(1,49)
d0 = csMax.c.item(0,49)
print(a0,b0,c0,d0)
