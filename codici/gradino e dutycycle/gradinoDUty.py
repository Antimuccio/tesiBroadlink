import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from datetime import datetime
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
import datetime

df=pd.read_csv("gradino.csv" ,sep = ",",dayfirst=True,parse_dates=['data'], index_col='data')
listaore=[]
dutycycle=0;
tempoinattivo=0;
vettoreduty=[];
indiciduty=[];
indici=[]
picco=0
scatta=0
for i in range (0,df.size):
 indici.append(df.index[i])
 if df.value[i]<=1:
    picco=0
    tempoinattivo+=120;
    listaore.append(0)
 else :
    dutycycle+=120
    if df.value[i]>picco:
     picco=df.value[i]
    listaore.append(picco*0.010)
    if df.value[i-1]<1:
     scatta+=1
 if scatta%2==0 and scatta!=0:
  vettoreduty.append(dutycycle/(dutycycle+tempoinattivo))
  indiciduty.append(df.index[i-1])
  scatta+=1
  dutycycle=0;
  tempoinattivo=0;

plt.plot(indici,listaore)
plt.plot(df.index,df.value/100,marker='o')
plt.plot(indiciduty,vettoreduty,linestyle=':',marker='*')
plt.xlabel('ora')
plt.ylabel('valori assoluti in scala')
plt.title('Variazione Dutycyle in giornata tipo')
plt.show()
