from tkinter import *
from tkcalendar import Calendar,DateEntry
from tkinter import messagebox, ttk
import tkinter as tk
import os
import sys
import csv


# rutapython = os.path.abspath(sys.argv[1])
# rutapython=os.path.abspath("C:/Venancio/python")
rutapython="C:/Users/cyt2/Documents/Venancio/Body/python"
rutapython = rutapython.replace("/", "\\")
#archivo = open (rutapython+"\\Formulario.txt", encoding="utf8")
#LLAMAMOS LA FUNCION SEND DATA
def send_data():
    segmento_data=segmento.get()
    eps_data=eps.get()
    #nit_data=nit.get()
    fechaini_data=fechaini.get()
    fechafi_data=fechafi.get()
    codigo_data=codigo.get()
    radicado_data=radicado.get()
    
    #GUARDAR INFORMACION DEL FORMULARIO EN UN ARCHIVO DE TEXTO
    #archivo=open("\FacturasRadicar\Formulario.txt", "w")
    archivo=open(rutapython+"\\Formulario.txt", "w")
    archivo.write(eps_data)
    archivo.write("-")
    #archivo.write(nit_data)
    #archivo.write("-")
    archivo.write(fechaini_data)
    archivo.write("-")
    archivo.write(fechafi_data)
    archivo.write("-")
    archivo.write(codigo_data)
    archivo.write("-")
    archivo.write(segmento_data)
    archivo.write("-")
    archivo.write(radicado_data)
    archivo.close()
    
    #BORRAR LOS CAMPOS DE LOS CUADROS DE TEXTO
    eps_entry.delete(0,END)
    #nit_entry.delete(0,END)
    fechaini_entry.delete(0,END)
    fechafi_entry.delete(0,END)
    codigo_entry.delete(0,END)
    segmento_entry.delete(0,END)
    radicado_entry.delete(0,END)

#CONFIGURAMOS LA VENTANA #3b6077
ventana= tk.Tk()
ventana.config(background='white')
ventana.geometry('450x600')
ventana.resizable(False,False)
ventana.title('Guardar Datos Entidades')
main_tittle=Label(text='Formulario Radicacion', font=("font='sans 12 bold'",15), bg="#005c68", fg="white", width="550", height="2")
main_tittle.pack()


#ETIQUETAS DE LOS NOMBRES DE LOS ENCABEZADOS

username_label= Label(text='EPS', bg="white",font='sans 10 bold')
username_label.place(x=22, y=70)
#username_label= Label(text='NIT', bg="white",font='sans 12 bold')
#username_label.place(x=22, y=130)5
username_label= Label(text='FechaInicial', bg="white",font='sans 12 bold')
username_label.place(x=22, y=130)
username_label= Label(text='FechaFinal', bg="white",font='sans 12 bold')
username_label.place(x=22, y=190)
username_label= Label(text='CodigoPlan', bg="white",font='sans 12 bold')
username_label.place(x=22, y=250)
username_label= Label(text='Radicado', bg="white",font='sans 12 bold')
username_label.place(x=22, y=310)
username_label= Label(text='Segmento', bg="white",font='sans 12 bold')
username_label.place(x=22, y=370)

#DEFINIMOS VARIABLES UTILIZANDO LA CLASE STRINVAR SE GUARDAN LOS DATOS QUE SE INGRESAN POR EL FORMULARIO

eps = StringVar()
nit = StringVar()
fechaini = StringVar()
fechafi = StringVar()
codigo = StringVar()
segmento = StringVar()
radicado=StringVar()

eps_entry= ttk.Combobox(textvariable=eps, width="40",font='sans 12 bold')
#nit_entry= ttk.Combobox(textvariable=nit, width="40",font='sans 12 bold')
#nit_entry= Entry(textvariable=fechaini, width="40")
fechaini_entry= DateEntry(ventana,textvariable=fechaini, width="40", year=2023,font='sans 12')
fechafi_entry= DateEntry(textvariable=fechafi, width="40", year=2023,font='sans 12')
codigo_entry= ttk.Combobox(textvariable=codigo, width="40",font='sans 12 ')
radicado_entry= Entry(textvariable=radicado, width="40",font='sans 12 bold')
segmento_entry= ttk.Combobox(textvariable=segmento, width="40",font='sans 12 bold')


#LISTA DEL COMBOBOX DE LA EPS
eps_entry["values"]=("Sura","NuevaEPS",'SaludTotal','SaviaSalud','RedVital',"Sura Soat","Sura ARL","Colmena","Coosalud","SegurosDelEstado")
#nit_entry["values"]=("800088702","900156264","8000130907","90064350")
#codigo_entry["values"]=("270.SURA CONTRIBUTIVO","347.SURA SUBSIDIADO","258.NUEVA CONTRIBUTIVO","354.NUEVA SUBSIDIADO","390.SAVIA CONTRIBUTIVO EVENTO","30.SALUD TOTAL CONTRIBUTIVO","343.SALUD TOTAL SUBSIDIADO")

codigo_entry["values"]=("30.SALUD TOTAL CONTRIBUTIVO",
                        "77.SURA COMPANIA SURAMERICANA DE SEGUROS (SOAT)",
                        "102.RED VITAL FONDO FASIVO SOCIAL DE FERROCARRILES NACIONALES DE COLOMBIA",
                        "258.NUEVA CONTRIBUTIVO",
                        "270.SURA CONTRIBUTIVO",
                        "271.SURA SEFUROS DE RIESGOS PROFESIONALES",
                        "324.SAVIA CONTRIBUTIVO",
                        "343.SALUD TOTAL SUBSIDIADO",
                        "347.SURA SUBSIDIADO",                        
                        "354.NUEVA SUBSIDIADO",
                        "390.SAVIA CONTRIBUTIVO EVENTO",
                        "393.REDVITAL",
                        "517.SAVIA SUBSIDIADO"
                        )

segmento_entry["values"]=("1.Generar Archivo Fact A Radicar",
                          "2.Generar Radicado Xenco",
                          "3.Descargar y Leer Ord de Servicio",
                          '4.Armado de Cuenta',
                          '5.Generar RIPS',
                          "6.Carga de RIPS",
                          "7.Comprimidos",
                          "8.Carga de Soportes",
                          "9.Corregir RIPS")

#DEFINIMOS LA UBICACION DE LOS CAMPOS DONDE SEVA A INGRESAR LOS DATOS

eps_entry.place(x=22, y=100)
#nit_entry.place(x=22, y=160)
fechaini_entry.place(x=22, y=160)
fechafi_entry.place(x=22, y=220)
codigo_entry.place(x=22, y=280)
radicado_entry.place(x=22, y=340)
segmento_entry.place(x=22, y=400)

#SE DEFINE TIPO CLASE Y SE CAPTURA LO QUE MUESTRA EL CALENDARIO EN FECHA INICIAL
def my_upd(*args):
    l1.config(text=fechaini.get())
#SE DEFINE TIPO CLASE Y SE CAPTURA LO QUE MUESTRA EL CALENDARIO EN FECHA FINAL
def my_upd2(*args):
    l2.config(text=fechafi.get())
#SE DEFINE TIPO CLASE Y SE CAPTURA LO QUE MUESTRA EL CALENDARIO EN FECHA FINAL
# def my_upd2(*args):
#     l3.config(text=eps.get())



#DEFINIMOS LAS UBICACIONES DEL CAMPO DE LA FECHA INICIAL EN CAMPO AMARILLO
l1=Label(ventana,bg='yellow')
l1.place(x=320, y=160)
#DEFINIMOS LAS UBICACIONES DEL CAMPO DE LA FECHA INICIAL EN CAMPO AMARILLO
l2=Label(ventana,bg='yellow')
l2.place(x=320, y=220)



#DEFINIMOS LAS UBICACIONES DEL CAMPO DE LA FECHA INICIAL EN CAMPO AMARILLO
# l3=Label(ventana,bg='yellow')
# l3.place(x=320, y=100)





#CREAMOS BOTON PARA GUARDAR LOS DATOS
boton= Button(ventana, text="Guardar", command=send_data, width="40", height="2", bg="green",justify='center',font='sans 11 bold',highlightcolor='yellow', fg="white")
boton.place(x=22, y=460)
#CREAMOS BOTOS PARA SALIR DEL FORMULARIO
botonsalida= Button(ventana, text="Salir", command=exit, width="40", height="2", bg="red",font='sans 11 bold',justify='center',highlightcolor='yellow',fg="white")
botonsalida.place(x=22, y=540)

#HACEMS EL LLAMADO DEL METODO FECHA INICIAL
fechainicial=fechaini.trace('w', my_upd)
#HACEMS EL LLAMADO DEL METODO FECHA INICIAL
fechafinal=fechafi.trace('w', my_upd2)
#HACEMS EL LLAMADO DEL METODO FECHA INICIAL
#epscombo=eps.trace('w', my_upd2)

ventana.mainloop()
