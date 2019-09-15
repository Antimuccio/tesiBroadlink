import broadlink
import time
import sys, string
import http.client
import tkinter as tk
import tkinter.ttk as ttk
import datetime
###apikey="97be21a66f75f38ee46e35f083833b71"
###nodeid= 395229
###conn.request("GET", "https://emoncms.org/input/post.json?apikey="+apikey+"&node="+str(nodeid)+"&csv="+valore)
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
 timer1=timerI-datetime.datetime.now().hour;
 timer2=timerF-datetime.datetime.now().hour;
 timer3=timerF-timerI;
 if (timer3>0 and timer1<=0) or (timer3<0 and timer2<0 and timer1<=0) or (timer3<0 and timer2>0 and timer1>=0):
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
     print(datetime.datetime.now(),valore,conn.getresponse().read())
     conn.close()
     var1.set(valore)
     indice=indice+1
     var2.set(datetime.datetime.now().strftime("%H:%M"))
     tk.Label(page2,text=str(valore)+" "+str(datetime.datetime.now().strftime("%D %H:%M")),relief="flat").grid(row=indice%10,column=1)
     idOp=finestra.after(120000,start)
 else:
     stop()

   
def stop():
    B1.config(state="active")
    devices[0].set_power(False);
    print("Spento"+str(datetime.datetime.now()))
    conn.request("GET", "http://localhost:8289/emoncms/input/post?node=2&fulljson={%22Frigo%22:"+"0"+"}&apikey=2537acbf42ca48a2e186dbb02b4f1b3e")
    conn.close()
    stato()
    var1.set("0")
    tk.Label(page2,textvar=var1,relief="flat").grid(row=indice%10,column=1)
    var2.set(datetime.datetime.now().strftime("%H:%M"))
    try:
     finestra.after_cancel(idOp)
    except:
         print("nulla da cancellare")
    if is_checked.get():
     if(timerI<=datetime.datetime.now().hour):
      differenza=(-datetime.datetime.now().hour+timerI+24)*3600000-datetime.datetime.now().minute*60000
     else:
      differenza=(-datetime.datetime.now().hour+timerI)*3600000-datetime.datetime.now().minute*60000
     print(round(differenza/3600000,2))
     finestra.after(differenza,start)
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
          timerI=int(a)
          timerF=int(b)
    else:
     timerI=-1;
     timerF=25;
      


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
timerI=-1
indice=0
timerF=25
stato()
if(devices[0].check_power()):
          start();
finestra.mainloop()


  
