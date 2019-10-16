import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from datetime import datetime
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
import datetime

dfT=pd.read_csv("Settembre.csv" ,sep = ",",dayfirst=True,parse_dates=['data'], index_col='data')
df=pd.read_csv("potenze.csv" ,sep = ",",dayfirst=True,parse_dates=['data'], index_col='data')
df2=df.resample('D').sum().dropna()
df2=df2[df2['value'] != 0]
plt.plot(dfT.index,dfT.value,marker='*',label='temperatura')
plt.ylabel('°C')

plt.show()
listaore=[]
totaleCamp=0;
i=0
for j in range (0,df2.size):
 contatore=0
 campioniD=0
 while df.index[i].day==df.index[i+1].day:
   campioniD+=1
   if df.value[i]>30:
    contatore=contatore+1
   if(i<df.size-2):
    i+=1
   if(i>=df.size-2):
    break;
 i+=1
 totaleCamp+=campioniD
 if(campioniD<720-72):
   listaore.append(0)
 else:
   listaore.append(contatore*120*100/86400)
plt.bar(df2.index,listaore, align='center', alpha=0.5,label='duty cycle %')
plt.xlabel('giorno')
plt.ylabel('valore medio')
plt.title('Legame tempo di funzionamento medio e temperatura')
plt.plot(dfT.index,dfT.value,marker='*',label='temperatura°C')
plt.legend(loc='upper left')
plt.show()
print(totaleCamp*120/86400) #tempo totale di monitoraggio stimato 
