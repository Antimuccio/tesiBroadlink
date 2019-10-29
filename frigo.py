import broadlink
import time
import sys, string
import http.client
import tkinter as tk
import tkinter.ttk as ttk
from datetime import datetime
import numpy as np

def stato():
     if(devices[0].check_power()):
       var.set("Stato Attuale Dispositivo: "+"Acceso")
     else:
      var.set("Stato Attuale Dispositivo: "+"Spento")
def start():
 global indice
 global idOp
 valore=None
 B1.config(state='disabled')
 ora=datetime.now().strftime("%H:%M")
 ora=datetime.strptime(ora,"%H:%M")
 timer1=(timerI-ora)
 if(timer1.days<0):
  timer1=(timer1).seconds*(timer1).days
 else:
  timer1=(timer1).seconds
 timer2=(timerF-ora)
 if(timer2.days<0):
  timer2=(timer2).seconds*(timer2).days
 else:
  timer2=(timer2).seconds
 timer3=timerF-timerI
 if(timer3.days<0):
  timer3=(timer3).seconds*(timer3).days
 else:
  timer3=(timer3).seconds
 if (timer3>0 and timer1<=0 and timer2>0) or (timer3<0 and timer2<0 and timer1<=0) or (timer3<0 and timer2>0 and timer1>=0) or timer3==0:
     while(True):
      try:
         if not devices[0].check_power():
          devices[0].set_power(True);
          valore=0
          stato()
         else:
           valore=round((devices[0].get_energy()),1)
         break;
      except:
            print("Errore lettura stato")
            time.sleep(5)
     conn.request("GET", "http://localhost:8289/emoncms/input/post?node=2&fulljson={%22Frigo%22:"+str(valore)+"}&apikey=2537acbf42ca48a2e186dbb02b4f1b3e")
     print(datetime.now(),valore,conn.getresponse().read())
     conn.close()
     var1.set(valore)
     indice=indice+1
     var2.set(datetime.now().strftime("%H:%M"))
     tk.Label(page2,text=str(valore)+" "+str(datetime.now().strftime("%D %H:%M")),relief="flat").grid(row=indice%10,column=1)
     idOp=finestra.after(120000,start)
 else:
     stop()

   
def stop():
    B1.config(state="active")
    devices[0].set_power(False);
    print("Spento"+str(datetime.now()))
    conn.request("GET", "http://localhost:8289/emoncms/input/post?node=2&fulljson={%22Frigo%22:"+"0"+"}&apikey=2537acbf42ca48a2e186dbb02b4f1b3e")
    conn.close()
    stato()
    var1.set("0")
    tk.Label(page2,textvar=var1,relief="flat").grid(row=indice%10,column=1)
    var2.set(datetime.now().strftime("%H:%M"))
    try:
     finestra.after_cancel(idOp)
    except:
         print("nulla da cancellare")
    if is_checked.get():
     ora=datetime.now().strftime("%H:%M")
     ora=datetime.strptime(ora,"%H:%M")
     differenza=(timerI-ora).seconds
     print(differenza)
     finestra.after(differenza*1000,start)
def aggiungisveglia():
    checkBoxName.set(mystring1.get()+"-"+mystring2.get())
    checkbox=tk.Checkbutton(page1,textvar=checkBoxName,command=settimer,onvalue=1,offvalue=0,variable=is_checked)
    checkbox.grid(row=30,column=120)
    is_checked.set(False);
def settimer():
    global timerI
    global timerF
    if(is_checked.get()):
      appoggio=checkBoxName.get()
      [a,b]=appoggio.split("-",1)
      try:
          timerI=datetime.strptime(a,"%H:%M")
      except:
          timerI=datetime.strptime("00:00","%H:%M")

      try:
          timerF=datetime.strptime(b,"%H:%M")
      except:
          timerF=datetime.strptime("00:00","%H:%M")
    else:
     timerI=datetime.strptime("00:00","%H:%M")
     timerF=datetime.strptime("00:00","%H:%M")


##grafica##
finestra=tk.Tk();
rows = 0
while rows < 50:
    finestra.rowconfigure(rows, weight=1)
    finestra.columnconfigure(rows, weight=1)
    rows += 1
var=tk.StringVar()
var1=tk.StringVar()
var2=tk.StringVar()
mystring1=tk.StringVar()
mystring2=tk.StringVar()
is_checked=tk.BooleanVar()
checkBoxName=tk.StringVar()
finestra.title("Broadlink")
finestra.geometry("400x300")
timer=ttk.Notebook(finestra)
timer.grid(row=1, column=0, columnspan=50, rowspan=49, sticky='NESW')
page1 = ttk.Frame(timer)
page2 = ttk.Frame(timer)
timer.add(page1, text='Controlli')
timer.add(page2, text='Log')
B1=tk.Button(page1,text="Avvia",width=12,relief="raised",command=start)
B1.place(x=0,y=0)
B2=tk.Button(page1,text="Stop",width=12,relief="raised",command=stop).place(x=100,y=0)
statoattuale=tk.Label(page1, textvar=var, relief="raised").place(x=180,y=50)
tk.Label(page1, text="Valore:").grid(row=0, sticky="w",pady=28)
tk.Label(page1, text="Ora:").grid(row=1, sticky="w",pady=2) 
l1 = tk.Label(page1,textvar=var1,relief="sunken",width=10).grid(row=0,column=1)
l2 = tk.Label(page1,textvar=var2,relief="sunken",width=10).grid(row=1,column=1)
tk.Label(page1, text="Inizio:").grid(row=3, sticky="w",pady=20)
tk.Label(page1, text="Fine:").grid(row=4, sticky="w",pady=0)
e1 =tk.Entry(page1,textvariable = mystring1).grid(row=3,column=1)
e2 =tk.Entry(page1,textvariable = mystring2).grid(row=4,column=1)
B3=tk.Button(page1,text="AggiungiTimer",width=12,relief="raised",command=aggiungisveglia).place(x=250,y=150)

##########MAIN######
while True:
 try:
     conn=http.client.HTTPConnection("localhost:8289")
     devices=broadlink.discover(timeout=4)
     devices[0].auth()
     break;
 except:
     print("Errore WebServer o SP")
     time.sleep(5)
timerI=datetime.strptime('00:00',"%H:%M")
indice=0
timerF=datetime.strptime('00:00',"%H:%M")
stato()
if(devices[0].check_power()):
          start();
finestra.mainloop()


  
