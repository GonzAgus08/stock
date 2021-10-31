from tkinter import *
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from PIL import ImageTk, Image



class programa():

    def __init__(self) -> None:    
        
        self.max=0
        self.cont=0
        self.lista=[]
        self.compraS=[]
        self.dias=[]
        global pantalla
        pantalla=Tk()
        pantalla.geometry("750x640")
        pantalla.title("CALCUULADORA")
        self.image= Image.open("./plot.png")
        self.image= self.image.resize((500,400), Image.ANTIALIAS)
        pantalla.config(background="light grey")
        self.img=ImageTk.PhotoImage(self.image)
        self.label=Label(pantalla,image=self.img)
        self.label.pack()
        self.texto=StringVar()
        self.texto.set(f"El stock se acabara en un rango de {self.max} dias: ")
        self.texto1=StringVar()
        self.texto1.set(f"Ventas dia {self.cont}")
        self.texto2=StringVar()
        self.texto2.set(f"compras dia {self.cont}")
    

        Label(
                    textvariable=self.texto,
                    bg="navy",
                    fg="white",
                    width="300",
                    height="3",
                    font=("calibri",15)
                ).pack()
    
        if self.cont==0:
            Label(text="stock inicial",background="light grey").pack()
            self.stock=Entry(pantalla)
            self.stock.pack()

            Button(
                        pantalla,
                        text="Ingresar",
                        height="3",
                        width=30,
                        command=self.post_stock
                    ).pack()
        else:
            self.post_stock()

    def post_stock(self):
            
        Label(textvariable=self.texto1,background="light grey").pack()
        self.ventas=Entry(pantalla)
        self.ventas.pack()
        Label(textvariable=self.texto2,background="light grey").pack()
        self.compras=Entry(pantalla)
        self.compras.pack()

        Button(
                    pantalla,
                    text="Continuar",
                    height="3",
                    width=30,
                    command=self.calcular                
                    ).pack()

    def calcular(self):

        self.cont+=1
        self.dias.append(self.cont)
        self.lista.append(int(self.ventas.get()))
        self.compraS.append(int(self.compras.get()))
        arrayy=np.array(self.lista)
        arrayy2=np.array(self.compraS)
        promedio=np.mean(arrayy)
        stdd=np.std(arrayy)

        for i in self.lista:
            if i > promedio+stdd or i<promedio-stdd:
                if i>promedio and promedio-(i/len(self.lista))>0:
                    promedio-=(i/len(self.lista))
                elif i>promedio and promedio-(i/len(self.lista))<=0:
                    mediana=np.median(arrayy)
                    var=mediana/promedio
                    promedio-=var
                elif i<promedio:
                    promedio+=(i/len(self.lista))

        detend=(int(self.stock.get()))-np.sum(arrayy)+np.sum(arrayy2)
        self.max=int(detend/promedio)

        dic={
            'dias': self.dias,
            'ventas': self.lista,
            'compras': self.compraS            
        }

        df=pd.DataFrame(dic)
        df.set_index('dias', inplace=True)
        df[['ventas','compras']].plot(kind="area", stacked=True)
        plt.savefig('plot.png')
        self.texto.set(f"El stock se acabara en un rango de {self.max} dias: ")
        self.texto1.set(f"ventas dia {self.cont}")
        self.texto2.set(f"compras dia {self.cont}")
        pantalla.update()

pantalla1=programa()
pantalla.mainloop()
