import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from datetime import datetime
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
import datetime

df=pd.read_csv("gradino2.csv" ,sep = ",",dayfirst=True,parse_dates=['data'], index_col='data')
listaore=[]
tempoattivo=0;
tempoinattivo=0;
vettoreduty=[];
indiciduty=[];
indici=[]
valorigradino=[]
j=0
media=0
scatta=0
for i in range (0,df.size):
 if(df.value[i]>1):
  media+=df.value[i]
  if(df.value[i-1]<1):
   j=i
 elif(df.value[i]<1 and df.value[i-1]>1):
  valorigradino.append(media/(i-j))
  media=0
  print(valorigradino[-1],i,j,i-j)
j=0
for i in range (0,df.size-1):
 indici.append(df.index[i])
 if df.value[i]<=1:
    picco=0
    tempoinattivo+=120;
    listaore.append(0)
    if scatta%2==1 and j<len(valorigradino)-1 and df.value[i-1]>1:
     j+=1
 else :
    tempoattivo+=120
    listaore.append(valorigradino[j]*0.01)
    if df.value[i-1]<1:
     scatta+=1
 if scatta%2==0 and scatta!=0:
  vettoreduty.append(tempoattivo/(tempoattivo+tempoinattivo))
  indiciduty.append(df.index[i-1])
  scatta+=1
  media=0
  tempoattivo=0;
  tempoinattivo=0;


plt.plot(indici,listaore,label='gradino simulato')
plt.plot(df.index,df.value/100,marker='o',label='consumi')
plt.plot(indiciduty,vettoreduty,linestyle=':',marker='*',label='duty cycle')
plt.xlabel('ora')
plt.ylabel('valori assoluti in scala')
plt.title('Variazione Duty cyle in giornata tipo')
plt.legend()
plt.show()
