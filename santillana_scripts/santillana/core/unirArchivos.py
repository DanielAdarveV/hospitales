from PyPDF2 import PdfFileMerger
import os

factura='13432'
ruta = r'C:\LUCHO\NUEVA EPS\2023-03\01\SU-1447054'
pdfs = [archivo for archivo in os.listdir(ruta) if archivo.endswith(".pdf")]
nombre_archivo_salida = factura+".pdf"
fusionador = PdfFileMerger()

for pdf in pdfs:
    fusionador.append(open(pdf, 'rb'))

with open(nombre_archivo_salida, 'wb') as salida:
    fusionador.write(salida)