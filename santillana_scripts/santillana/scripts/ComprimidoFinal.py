import os
from PyPDF2 import PdfMerger, PdfReader,PdfWriter
from PyPDF2.errors import PdfReadError
import locale
from pathlib import Path
import datetime
from babel.dates import format_date

#Objetos para la manipulacion de los PDF 

objEntidad={
  "SS400": [
    {
      "id": 1,
      "nomenclatura": "FE#NumFactura",
      "carpetaGuardar": "Soportes",
      "carpetaContenedor":"FE#NumFactura",
      "soportes": [
        "factura",
        "autorizacion",
        "historia_clinica",
        "material_osteosintesis",
        "quirurgicos",
        "medicamentos",
        "insumos",
        "resultados_examenes",
        "furips",
        "soat",
        "otros"
      ]
    }
  ]
}

objGrupos={
  "autorizacion": [
    "auto",
    "anexo",
    "remision"
  ],
  "factura": [
    "fac"
  ],
  "historia_clinica": [
    "epi",
    "hc",
    "hev",
    "consu",
    "form",
    "hemod"
  ],
  "insumos": [
    "gastos urg",
    "insumos rx",
    "cardio",
    "transfusion"
  ],
  "material_osteosintesis": [
    "maos"
  ],
  "medicamentos": [
    "aplicacion med",
    "hoja gastos",
    "oxi",
    "oxigeno",
    "formula"
  ],
  "otros": [
    "documento",
    "validacion",
    "consentimiento",
    "traslado"
  ],
  "quirurgicos": [
    "dqx",
    "insumos dqx",
    "anestesia"
  ],
  "resultados_examenes": [
    "lab",
    "rx",
    "electro",
    "ekg",
    "gluco",
    "soportes ext"
  ],
  "soat": [
    "soat"
  ],
  "furips": [
    "furips"
  ]
}



def crearCarpeta(rutaBase,nombreCarpeta):
    """
    Crea la carpeta de soportes en la ruta especificada.

    Parámetros:
    rutaBase (str): La ruta base donde estan los soportes a comprimir.
                     Puede ser una ruta absoluta o relativa.
    nombreCarpeta (str): El nombre de la carpeta a crear.

    Retorna:
    None
    """

    # Verifica si la carpeta ya existe
    if not os.path.exists(rutaBase+"\\"+nombreCarpeta):
        # Si no existe, la crea
        os.makedirs(rutaBase+"\\"+nombreCarpeta)
        print(f"Carpeta creada en: {rutaBase}\\{nombreCarpeta}")
    else:
        print(f"La carpeta ya existe en: {rutaBase}\\{nombreCarpeta}")

def listar_carpetas(rutaBase):
    """
    Lista todas las carpetas dentro de una carpeta dada.

    Parámetros:
    rutaBase (str): La ruta de la carpeta que contiene otras carpetas.

    Retorna:
    List[str]: Una lista con los nombres de las carpetas dentro de la carpeta base.
    """
    carpetas = []
    
    # Verifica si la ruta base existe
    if os.path.exists(rutaBase) and os.path.isdir(rutaBase):
        # Recorre los elementos en la carpeta base
        for item in os.listdir(rutaBase):
            ruta_completa = os.path.join(rutaBase, item)
            # Si es un directorio, lo añade a la lista de carpetas
            if os.path.isdir(ruta_completa):
                carpetas.append(item)
    
    return carpetas

def unirPdf(rutaCarpeta, carpetaSalida, nombreFactura,entidad):
    
    # Obtenemos todos los soportes que deberan quedar al final
    soportes = objEntidad[entidad]

    # Recorremos los soportes
    for soporteFinal in soportes:
        print(soporteFinal["soportes"])
        grupoSoportes = soporteFinal["soportes"]

        # Nomenclatura y nombre del archivo final
        nomenclatura = soporteFinal["nomenclatura"]
        #Reemplazamos posibles variables
        nombreFinal = nomenclatura.replace("#NumFactura", nombreFactura)

        #Validar si el soporte va dentro de otra carpeta, aparte de la de soportes Finale 
        carpetaContenedor= soporteFinal["carpetaContenedor"]
        carpetaContenedor = carpetaContenedor.replace("#NumFactura", nombreFactura)

        #Validar si  debe ir dentro de una carepta, si no exite se crea y define la ruta de salida        
        if carpetaContenedor== "": 
            # Define la ruta de salida
            ruta_salida = os.path.join(carpetaSalida, f'{nombreFinal}.pdf')
            
        else:
          crearCarpeta(carpetaSalida,carpetaContenedor)
          # Define la ruta de salida
          ruta_salida = os.path.join(carpetaSalida,carpetaContenedor, f'{nombreFinal}.pdf')

        # Crea una instancia nueva del objeto PdfMerger para cada soporte
        merger = PdfWriter()

        for grupo in grupoSoportes:
            orden_deseado = objGrupos[grupo]
            
            # Recorre el orden deseado y agrega los archivos correspondientes
            for prefijo in orden_deseado:
                # Recorre todos los archivos en la carpeta de entrada
                for archivo in os.listdir(rutaCarpeta):
                    if archivo.lower().endswith('.pdf') and archivo.lower().startswith(prefijo):
                        ruta_archivo = os.path.join(rutaCarpeta, archivo)
                        print(ruta_archivo)
                        # Verifica si el archivo existe
                        if os.path.exists(ruta_archivo):
                            try:
                                # Agrega mensajes de depuración para los archivos más grandes
                                archivo_size = os.path.getsize(ruta_archivo) / (1024 * 1024)  # Tamaño en MB
                                print(f'\n Tamaño del archivo: {archivo} es {archivo_size:.2f} MB')

                                # Intentamos abrir el archivo para verificar si está corrupto
                                # with open(ruta_archivo, 'rb') as f:
                                #     reader = PdfReader(f) # Se lee el archivo PDF
                                #     _ = reader.numPages

                                # Si el archivo es válido, se agrega al merger
                                print(f'Agregando: {archivo} desde {ruta_archivo}')
                                merger.append(ruta_archivo)
                                print("Se agrego correctamente!!")

                            except (PdfReadError, OSError) as e:
                                # Si hay un error, se registra pero no se detiene el proceso
                                print(f'Error al agregar {archivo}: archivo corrupto o inaccesible ({e})')
                        else:
                            print(f'Archivo no encontrado: {ruta_archivo}')

        # Verifica que haya archivos para combinar antes de escribir el archivo final
        if len(merger.pages) > 0:
            # Escribe el archivo PDF combinado en la ruta de salida
            try:
                merger.write(ruta_salida)
                print(f'Archivos combinados en: {ruta_salida}')
            except Exception as e:
                print(f'Error al escribir el archivo combinado: {e}')
            finally:
                merger.close()  # Asegura que el merger se cierre correctamente
        else:
            print(f'No se encontraron archivos PDF válidos para combinar en {ruta_salida}')
            merger.close()

def ComprimirEndPoint(rutaBase,factura,entidad):
    
    crearCarpeta(rutaBase,"SOPORTES")

    rutaCarpetaSalida= rutaBase+"\\"+"SOPORTES"
    rutaCarpeta= rutaBase+"\\"+factura

    unirPdf(rutaCarpeta,rutaCarpetaSalida,factura,entidad)

def ComprimirManual(rutaBase,entidad):
    
    crearCarpeta(rutaBase,"SOPORTES")

    rutaCarpetaSalida= rutaBase+"\\"+"SOPORTES"
    carpetas = listar_carpetas(rutaBase)

    for carpeta in carpetas:
      rutaCarpeta= rutaBase+"\\"+carpeta

      unirPdf(rutaCarpeta,rutaCarpetaSalida,carpeta,entidad)

# ruta = r"Y:\2024\septiembre\Sanitas\27802\196574" 
# rutaSalida = r"Y:\2024\septiembre\Sanitas\27802\Prueba"
# factura="Daniel"
# entidad="sanitas"

# unirPdf(ruta,rutaSalida,factura,entidad)

#Colocar el contrato_armar y la ruta base como parametros de entrada
contrato_Armar="SS400"
locale.setlocale(locale.LC_ALL, ("es_ES", "UTF-8"))

# Obtener la fecha actual
fecha_actual = datetime.datetime.now()

# Extraer el año y el mes
anio_actual = fecha_actual.year

    
# Obtener el nombre del mes en español usando Babel
mes_actual = format_date(fecha_actual, format='MMMM', locale='es_ES')
ruta_base = Path(f"Y:\\{anio_actual}\\{mes_actual}\\Sanitas\\Remision")
#rutaBase=r"Y:\2024\septiembre\Sanitas\Remision"
ComprimirManual(ruta_base,contrato_Armar)