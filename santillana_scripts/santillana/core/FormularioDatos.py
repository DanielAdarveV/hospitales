import pandas as pd
import psycopg2
import os
import sys
import csv

#TRAEMOS LA RUTA DESDE ELECTRONEEK VARIABLE COMO RUTA PYTHON
# rutapython = os.path.abspath(sys.argv[1])
rutapython="C:/Users/cyt2/Documents/Venancio/Body/python"
rutapython = rutapython.replace("/", "\\")
archivo = open (rutapython+"\\Formulario.txt", encoding="utf8")


#CARGAMOS EL ARCHIVO TXT
#archivo = open ("FacturasRadicar\Formulario.txt", encoding="utf8")#
# archivo = open ("C://VenancioFormulario.txt", encoding="utf8")
fila = csv.reader (archivo, delimiter="-")
listatabla=list(fila)
#CAMBIAMOS EL FORMATO DE TIPO OBJECT A STRING
cambiostrin=str(listatabla)
#REALIZAMOS UN SPLIT A LAS VARIABLES QUE TRAEMOS DEL FORMULARIO
separador=cambiostrin.split(',')
#print(separador)
eps=separador[0]
#nit=separador[1]
fechaini=separador[1]
fechafin=separador[2]
codigo=separador[3]
segmento=separador[4]
radicado=separador[5]
#LIMPIAMOS LA BASURA QUE TRAE EL ARCHIVO DE TEXTO O REEMPLAZAMOS VALORES
# if eps !='':    
#     eps='Vacio'
#     print("si")
# else:
#     eps=eps.replace('[[','')  
#     print('No') 
#eps=eps.replace("",'Vacio')
eps=eps.replace('[[','')
codigo=codigo.replace(']]','')
#nit=nit.replace(' ','')
fechaini=fechaini.replace(' ','')
fechaini=fechaini.replace('23','2023')
fechafin=fechafin.replace(' ','')
fechafin=fechafin.replace('23','2023')
codigo=codigo.replace(' ','')
segmento=segmento.replace(' ','')
radicado=radicado.replace(' ','')
radicado=radicado.replace(']]','')


Nit={
    "RedVital":"10617",
    "Sura":"800088702",
    "NuevaEPS":"900156264",
    "SaviaSalud":"90064350",
    "SaludTotal":"8000130907",
    "Coosalud":"00000",
    "Colmena":"00000",
    "Sura Soat":"800088702",
    "Sura ARL":"800088702",
    "SegurosDelEstado":"800088702"

}

nitEps=Nit[eps.replace("'",'')]
#print(eps)
#print(nit)
#print(fechaini)
#print(fechafin)
#print(codigo)
#print(segmento)
print(eps+"-"+fechaini+"-"+fechafin+"-"+codigo+"-"+segmento+"-"+radicado+"-"+nitEps)

