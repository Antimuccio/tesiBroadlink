import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from datetime import datetime
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
import datetime

df=pd.read_csv("potenze.csv" ,sep = ",",dayfirst=True,parse_dates=['data'], index_col='data')
dfP=pd.read_csv("76.csv" ,sep = ",",dayfirst=True,parse_dates=['data'], index_col='data')
listaore=[]
totaleCamp=0;
i=0
for j in range (0,dfP.size):
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
   listaore.append(dfP.value[j])
plt.bar(dfP.index,listaore, align='center', alpha=0.5)
plt.xlabel('giorno')
plt.ylabel('kWh')
plt.title('Consumi giornalieri')
plt.legend(loc='upper left')
plt.show()
 
