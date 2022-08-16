
import tkinter as tk
from tkinter import HORIZONTAL, Button, Entry, Label, Spinbox, StringVar, ttk
import math as ma
import tkinter
from tkinter import messagebox

class antena():
    def __init__(self, gain, u):
        
        self.gain = gain
        self.unit = u
        
        if u == "dBi":
            self.dBi = round(gain, 4)
            self.dBd = round((gain -2.15), 4)
        elif u == "dBd":
            self.dBi = round((gain +2.15) , 4)
            self.dBd = round(gain, 4)
        else :
            self.dBi = None
            self.dBd = None    
        
class potencia():
    def __init__(self, power, u):
        
        self.power = round(power, 4)
        self.unit = u
        
        if u == "W":
            self.watt =round(self.power,4)
            
            dBm =10*(ma.log10(self.watt)) + 30
            dBm = round(dBm,4)
            self.dBm = dBm
            
            self.dBW = round((self.dBm -30),4)

        elif u == "dBm":
            self.dBm = round((self.power),4)
            
            self.dBW = round((self.dBm -30),4)
            
            w = ma.pow(10, self.dBW/10)
            w = round(w,4)
            self.watt = w
        
        elif u == "dBW":
            self.dBW = round(self.power,4)
            
            self.dBm = round((self.dBW +30,4))
            
            w = ma.pow(10, self.dBW/10)
            w = round(w,4)
            self.watt = w   
        
        else:
            self.dBm = None
            self.dBW = None
            self.watt = None        

class sistema():
    def __init__(self, transmisor: potencia, radiante: antena, perdidas: potencia, pra:potencia):
        
        if pra == None:
            p = transmisor.dBm + radiante.dBd - perdidas.power
            self.pra = potencia(p, "dBm")

        if perdidas == None:
            l = transmisor.dBm + radiante.dBd -pra.dBm
            self.loss = potencia(l,"")

        if radiante == None:
            g = pra.dBm - transmisor.dBm + perdidas.power
            self.gain = antena(g, "dBd")

        if transmisor == None:
            tx = pra.dBm -radiante.dBd + perdidas.power
            self.tx = potencia(tx, "dBm")


unidadesPotencia = ("W", "dBm", "dBW")
unidadesGanancia = ("dBi", "dBd")

root =tkinter.Tk()
root.title("Calculadora de PRA")

valorPotencia = StringVar()
valorGanancia = StringVar()
valorPerdidas = StringVar()
valorPRA = StringVar()

calculoPotencia = StringVar()
calculoGanancia = StringVar()
calculoPerdidas = StringVar()
calculoPRA = StringVar()


def limpiar():
    entryPotencia.delete("0", "end")
    entryGanancia.delete("0", "end")
    entryPerdidas.delete("0", "end")
    entryPRA.delete("0", "end")
    
    LabelPCalculada.config(text="")
    LabelGCalculada.config(text="")
    LabelPerCalculada.config(text="")
    LabelPRACal.config(text="")

def calcularPotencia():
    try:
        gain = antena(float(entryGanancia.get()), spinGanancia.get())
        loss = potencia(float(entryPerdidas.get()), "")
        pra = potencia(float(entryPRA.get()), spinPRA.get())
        
        radio = sistema(None, gain, loss, pra)
        if spinPotenciaCalculada.get() == "W":
            calculoPotencia.set(radio.tx.watt)
        elif spinPotenciaCalculada.get() == "dBW":
            calculoPotencia.set(radio.tx.dBW)
        else:
            calculoPotencia.set(radio.tx.dBm)   
        LabelPCalculada.config(text= calculoPotencia.get())
    except: 
        mensaje = messagebox.showerror(title="Error", message="Ingrese los valores correctamente" ) 

        mensaje
     
def calcularGanancia():
    try:
        power = potencia(float(entryPotencia.get()), spinPotencia.get())
        loss = potencia(float(entryPerdidas.get()), "")
        pra = potencia(float(entryPRA.get()), spinPRA.get())
        
        radio = sistema(power, None, loss, pra)
        if spinGananciaCalculada.get() == "dBi":
            calculoGanancia.set(radio.gain.dBi)
        else:
            calculoGanancia.set(radio.gain.dBd)
        LabelGCalculada.config(text=calculoGanancia.get())       
    except:
        mensaje = messagebox.showerror(title="Error", message="Ingrese los valores correctamente" ) 

        mensaje
       
def calcularPerdidas():
    try:
        power = potencia(float(entryPotencia.get()), spinPotencia.get())
        gain = antena(float(entryGanancia.get()), spinGanancia.get())
        pra = potencia(float(entryPRA.get()), spinPRA.get())
        
        radio = sistema(power, gain, None, pra)
        calculoPerdidas.set(radio.loss.power)
        LabelPerCalculada.config(text = calculoPerdidas.get())
    except:
        mensaje = messagebox.showerror(title="Error", message="Ingrese los valores correctamente" ) 

        mensaje
      
def calcularPRA():
    try:
        power = potencia(float(entryPotencia.get()), spinPotencia.get())
        gain = antena(float(entryGanancia.get()), spinGanancia.get())   
        loss = potencia(float(entryPerdidas.get()), "")
        
        radio = sistema(power, gain, loss, None)
        if spinPRACalculadas.get() == "W":
            calculoPRA.set(radio.pra.watt)
        elif spinPRACalculadas.get() == "dBW":
            calculoPRA.set(radio.pra.dBW)
        else:
            calculoPRA.set(radio.pra.dBm)
        LabelPRACal.config(text=calculoPRA.get())
    except:
        mensaje = messagebox.showerror(title="Error", message="Ingrese los valores correctamente" ) 

        mensaje
         
labelValores = Label(text="Valores")
labelValores.grid(row="0", column="0", )

labelPotencia1 = Label(text="1. Potencia= ")
labelPotencia1.grid(row="1", column="0")

labelGanancia = Label(text="2. Ganancia= ")
labelGanancia.grid(row="2", column="0")

labelPerdidas = Label(text="3. Perdidas= ")
labelPerdidas.grid(row="3", column="0")

labelPRA = Label(text="4. Potencia aparente =")
labelPRA.grid(row="4", column="0")

entryPotencia = Entry(root)
entryPotencia.grid(row="1", column="1")


entryGanancia = Entry(root, textvariable="")
entryGanancia.grid(row="2", column="1")

entryPerdidas = Entry(root, textvariable="")
entryPerdidas.grid(row="3", column="1")

entryPRA = Entry(root, textvariable="")
entryPRA.grid(row = "4", column="1")

spinPotencia = Spinbox(root, values = unidadesPotencia )
spinPotencia.grid(row="1", column="2")

spinGanancia = Spinbox(root, values=unidadesGanancia)
spinGanancia.grid(row="2", column="2")

spinPerdidas = Spinbox(root, values="dB")
spinPerdidas.grid(row="3", column="2")

spinPRA = Spinbox(root, values=unidadesPotencia)
spinPRA.grid(row="4", column="2")

botonLimpiar = ttk.Button(root, text="limpiar", command=limpiar)
botonLimpiar.grid(row="3", column="3")

separador = ttk.Separator(root, orient=tk.HORIZONTAL)
separador.grid(row="6",column="0", sticky="EW")

separador1 = ttk.Separator(root, orient=tk.HORIZONTAL)
separador1.grid(row="7",column="0", sticky="EW")

calculoLabel = Label(root, text="Calculos")
calculoLabel.grid(row="7", column="0")

LabelPotenciaCalculada = Label(root, text="1. Potencia =")
LabelPotenciaCalculada.grid(row="8", column="0")

LabelGananciaCalculada = Label(root, text="2. Ganancia =")
LabelGananciaCalculada.grid(row="9", column="0")

LabelPerdidasCalculada = Label(root, text="3. Perdidas =")
LabelPerdidasCalculada.grid(row="10", column="0")

LabelPRACalculada = Label(root, text="4. PRA =")
LabelPRACalculada.grid(row="11", column="0")

LabelPCalculada = Label(root)
LabelPCalculada.grid(row="8", column="1")

LabelGCalculada = Label(root, textvariable="")
LabelGCalculada.grid(row="9", column="1")

LabelPerCalculada = Label(root, textvariable="")
LabelPerCalculada.grid(row="10", column="1")

LabelPRACal = Label(root, textvariable="")
LabelPRACal.grid(row="11", column="1")

spinPotenciaCalculada = Spinbox(root, values = unidadesPotencia )
spinPotenciaCalculada.grid(row="8", column="2")

spinGananciaCalculada = Spinbox(root, values=unidadesGanancia)
spinGananciaCalculada.grid(row="9", column="2")

spinPerdidasCalculadas = Spinbox(root, values="dB")
spinPerdidasCalculadas.grid(row="10", column="2")

spinPRACalculadas = Spinbox(root, values=unidadesPotencia)
spinPRACalculadas.grid(row="11", column="2")

botonCalcularPotencia = ttk.Button(root, text="Calcular Potencia", command=calcularPotencia)
botonCalcularPotencia.grid(row="8", column="3")

botonCalcularGanancia = ttk.Button(root, text="Calcular Ganancia", command=calcularGanancia)
botonCalcularGanancia.grid(row="9", column="3")

botonCalcularPerdidas = ttk.Button(root, text="Calcular Perdidas", command=calcularPerdidas)
botonCalcularPerdidas.grid(row="10", column="3")

botonCalcularPRA = ttk.Button(root, text="Calcular PRA", command=calcularPRA)
botonCalcularPRA.grid(row="11", column="3")

root.mainloop()




