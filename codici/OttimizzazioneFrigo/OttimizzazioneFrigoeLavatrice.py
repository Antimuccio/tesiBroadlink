from scipy import interpolate
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
import matplotlib.dates as mdates
import datetime

# serve per intersezione con spline
def temp (energia,media,inizio,fine,codice):
 x=np.linspace(inizio,fine,1000)
 nuovovalore=energia
 secondi=x[1]
 i=1
 if( codice==1):
     differenza=csMax(x[1])-nuovovalore
     while csMax(x[i])-nuovovalore>0:
      nuovovalore=energia+media*(x[i]-inizio)/3600000
      if (csMax(x[i])-nuovovalore)<differenza and csMax(x[i])-nuovovalore>0:
       secondi=x[i]
      i+=1
     secondi=secondi-inizio
 else:
     differenza=energia-csMin(x[i])
     while energia-csMin(x[i])>0:
      if energia-csMin(x[i])<differenza :
       secondi=x[i]
      i+=1
     secondi=secondi-inizio
 return secondi
##########
##dichiarazioni vari e conversioni necessarie per avere tutto in secondi normalizzato
originale=pd.read_csv("74.csv" ,sep = ",",dayfirst=True,parse_dates=['data'], index_col='data')
lavatrice=pd.read_csv('lavatrice.csv',sep=' ',parse_dates=['timestamp'], index_col='timestamp')
Frigo=pd.read_csv('frigo.csv',sep=' ',parse_dates=['timestamp'], index_col='timestamp')
Frigo.index = pd.to_datetime(Frigo.index, unit='s')
Frigo=Frigo[Frigo['value'] < 3000]
Frigo=Frigo[Frigo['value'] >=0]
Frigo=Frigo.resample('2T').pad().dropna()
lavatrice.index = pd.to_datetime(lavatrice.index, unit='s')
lavatrice=lavatrice[lavatrice['value'] < 3000]
lavatrice=lavatrice[lavatrice['value'] >=0]
lavatrice=lavatrice.resample('2T').pad().dropna()
ore=(mdates.date2num(originale.index)-mdates.date2num(originale.index[0]))*86400
oreFrigo=(mdates.date2num(Frigo.index)-mdates.date2num(Frigo.index[0]))*86400
oreLavatrice=(mdates.date2num(lavatrice.index)-mdates.date2num(lavatrice.index[0]))*86400
ValoriFrigo=Frigo.loc[Frigo.index].values
ValoriOriginale=originale.loc[originale.index].values
ValoriLavatrice=lavatrice.loc[lavatrice.index].values
ottimizzazione=[]
ottimizzazione.append(0)
indiciOtt=[]
indiciOtt.append(0)
EnergiaOttimizzazione=[]
EnergiaOriginale=[]
EnergiaOttimizzazione.append(0)
EnergiaOriginale.append(0)
fmin=[]
fmax =[]
prova=[]
minI=[]
maxI=[]
######
for i in range(0,len(ore)-1):
  EnergiaOriginale.append(EnergiaOriginale[-1]+ValoriOriginale[i]*120/3600000)
  EnergiaOriginale[i] = np.around(EnergiaOriginale[i],3)
for i in range(1,ore.size):
    if(i==ore.size-1):
       if EnergiaOriginale[i]-EnergiaOriginale[i-1]>0.001:
        fmax.append(EnergiaOriginale[i])
        maxI.append(ore[i])
    else:
     if EnergiaOriginale[i+1]-EnergiaOriginale[i]<0.001 and EnergiaOriginale[i]-EnergiaOriginale[i-1]>EnergiaOriginale[i+1]-EnergiaOriginale[i]:
        fmax.append(EnergiaOriginale[i])
        maxI.append(ore[i])
     if EnergiaOriginale[i]-EnergiaOriginale[i-1]<0.001 and EnergiaOriginale[i]-EnergiaOriginale[i-1]<EnergiaOriginale[i+1]-EnergiaOriginale[i] :
        fmin.append(EnergiaOriginale[i])
        minI.append(ore[i])
csMax=interpolate.PchipInterpolator(maxI,fmax)
csMin=interpolate.PchipInterpolator(minI,fmin)

##creazione ottimizzazione sfruttando potenza media monitorata
media=np.mean(originale[originale['value']>1].value)
aggiunta=(media*120/3600000)
flag=False
tempo=0
for i in range(0,len(ore)-1):
 condizioneInferiore=csMin(ore[i+1])-EnergiaOttimizzazione[-1]>0 and csMin(ore[i])-EnergiaOttimizzazione[-1]<0
 condizioneSuperiore=csMax(ore[i])>EnergiaOttimizzazione[-1] and csMax(ore[i+1])<EnergiaOttimizzazione[-1]+aggiunta  
 if EnergiaOriginale[i+1]==0:
   indiciOtt.append(ore[i+1])
   EnergiaOttimizzazione.append(EnergiaOttimizzazione[-1])
   ottimizzazione.append(0)
 else:
  if not flag:
      if ValoriFrigo[i]+np.max(ValoriOriginale)+ValoriLavatrice[i]<3000 or (condizioneInferiore):
       if condizioneSuperiore   :
        tempo=temp(EnergiaOttimizzazione[-1],media,ore[i],ore[i+1],1)
        EnergiaOttimizzazione.append(EnergiaOttimizzazione[-1]+media*tempo/3600000)
        indiciOtt.append(indiciOtt[-1]+int(tempo))
        ottimizzazione.append(media)
        flag=True
        indiciOtt.append(ore[i+1])
        EnergiaOttimizzazione.append(EnergiaOttimizzazione[-1])
        ottimizzazione.append(0)
       else:
        EnergiaOttimizzazione.append(EnergiaOttimizzazione[-1]+aggiunta)
        ottimizzazione.append(media)
        indiciOtt.append(ore[i+1])
      else:
       indiciOtt.append(ore[i+1])
       EnergiaOttimizzazione.append(EnergiaOttimizzazione[-1])
       ottimizzazione.append(0)
  else:
     if condizioneInferiore :
      flag=False
      tempo=temp(EnergiaOttimizzazione[-1],media,ore[i],ore[i+1],0)
      indiciOtt.append(indiciOtt[-1]+int(tempo))
      ottimizzazione.append(0)
      EnergiaOttimizzazione.append(EnergiaOttimizzazione[-1])
      indiciOtt.append(ore[i+1])
      ottimizzazione.append(media)
      EnergiaOttimizzazione.append(EnergiaOttimizzazione[-1]+media*(120-tempo)/3600000)
     else:
        indiciOtt.append(ore[i+1])
        EnergiaOttimizzazione.append(EnergiaOttimizzazione[-1])
        ottimizzazione.append(0)
######### 
#####
plt.suptitle('Ottimizzazione')
ax1=plt.subplot(211)
ax2=plt.subplot(212)
ax1.plot(ore,ValoriOriginale,label='originale')
ax1.plot(oreFrigo,ValoriFrigo,label="frigo")
ax1.plot(oreLavatrice,ValoriLavatrice,label="lavatrice")
ax1.step(indiciOtt,ottimizzazione,label="ottimizzazione")
ax1.set_xlabel('secondi')
ax1.set_ylabel('W')
ax1.legend()
ax2.plot(ore,csMax(ore),ore,csMin(ore))
ax2.plot(indiciOtt,EnergiaOttimizzazione,label="energia ottimizzazione")
ax2.plot(ore,EnergiaOriginale,label="energia originale")
ax2.legend()
ax1.set_xlabel('secondi')
ax1.set_ylabel('kWh')
plt.show()
