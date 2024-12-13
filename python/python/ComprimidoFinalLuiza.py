import os
import shutil
from PyPDF2 import PdfMerger, PdfReader, PdfWriter
from PyPDF2.errors import PdfReadError
import locale
from pathlib import Path
import datetime
import sys
from babel.dates import format_date

#Objetos para la manipulacion de los PDF 

objEntidad={
  "1": [
    {
      "id": 1,
      "nomenclatura": "FE#NumFactura",
      "carpetaGuardar": "Soportes",
      "carpetaContenedor":"",
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
  ],
  "2": [
    {
      "id": 1,
      "nomenclatura": "800219192_FE_#NumFactura",
      "carpetaGuardar": "FACTURAS",
      "carpetaContenedor":"",
      "soportes": [
        "factura"
      ]
    },
    {
      "id": 1,
      "nomenclatura": "800219192_FE_#NumFactura",
      "carpetaGuardar": "SOPORTES",
      "carpetaContenedor":"800219192_FE_#NumFactura",
      "soportes": [
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
  ],
  "3": [
    {
      "id": 1,
      "nomenclatura": "FE#NumFactura",
      "carpetaGuardar": "Factura",
      "carpetaContenedor":"",
      "soportes": [
        "factura"
      ]
    },
    {
      "id": 2,
      "nomenclatura": "FE#NumFactura_SOP_0",
      "carpetaGuardar": "Soportes",
      "carpetaContenedor":"",
      "soportes": [
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
  ],
  "4": [
    {
      "id": 1,
      "nomenclatura": "FE#NumFactura",
      "carpetaGuardar": "Facturas",
      "carpetaContenedor":"",
      "soportes": [
        "factura"
      ]
    },
    {
      "id": 1,
      "nomenclatura": "FE#NumFactura",
      "carpetaGuardar": "Soportes",
      "carpetaContenedor":"",
      "soportes": [
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
  ],
  "5": [
    {
      "id": 1,
      "nomenclatura": "FAC_FE#NumFactura_0",
      "carpetaGuardar": "Soportes",
      "carpetaContenedor":"",
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
  ],
  "6": [
    {
      "id": 1,
      "nomenclatura": "FACTURA #NumFactura",
      "carpetaGuardar": "Soportes",
      "carpetaContenedor":"",
      "soportes": [
        "factura"
      ]
    },
    {
      "id": 1,
      "nomenclatura": "SOPORTES FACTURA #NumFactura",
      "carpetaGuardar": "Soportes",
      "carpetaContenedor":"",
      "soportes": [
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
    if not os.path.exists(str(rutaBase)+"\\"+nombreCarpeta):
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

def crearDirectoriosGuardarSoportes( rutacarpetaBaseSalida, entidad):
    # Obtenemos todos los soportes que deberán quedar al final
    soportes = objEntidad[entidad]

    #Crear Carpetas donde se guardaran los soporte- Carpetas Generales
    for soporteFinal in soportes:
        
      carpeta_final = soporteFinal["carpetaGuardar"]
    
      crearCarpeta(rutacarpetaBaseSalida,carpeta_final)

def unirPdf(rutaCarpeta, rutacarpetaBaseSalida, nombreFactura, entidad):
    
    # Obtenemos todos los soportes que deberán quedar al final
    soportes = objEntidad[entidad]

    # Recorremos los soportes
    for soporteFinal in soportes:
        
        print(soporteFinal["soportes"])
        grupoSoportes = soporteFinal["soportes"]

        carpeta_final = soporteFinal["carpetaGuardar"]
        carpetaSalida=rutacarpetaBaseSalida+'\\'+carpeta_final

        # Nomenclatura y nombre del archivo final
        nomenclatura = soporteFinal["nomenclatura"]
        # Reemplazamos posibles variables
        nombreFinal = nomenclatura.replace("#NumFactura", nombreFactura)

        # Validar si el soporte va dentro de otra carpeta, aparte de la de soportes Finales 
        carpetaContenedor = soporteFinal["carpetaContenedor"]
        carpetaContenedor = carpetaContenedor.replace("#NumFactura", nombreFactura)

        # Validar si debe ir dentro de una carpeta, si no existe se crea y define la ruta de salida        
        if carpetaContenedor == "": 
            # Define la ruta de salida
            ruta_salida = os.path.join(carpetaSalida, f'{nombreFinal}.pdf')
        else:
            crearCarpeta(carpetaSalida, carpetaContenedor)
            # Define la ruta de salida
            ruta_salida = os.path.join(carpetaSalida, carpetaContenedor, f'{nombreFinal}.pdf')

        # Crea una instancia nueva del objeto PdfMerger para cada soporte
        merger = PdfMerger()

        for grupo in grupoSoportes:
            orden_deseado = objGrupos[grupo]
            
            # Recorre el orden deseado y agrega los archivos correspondientes
            for prefijo in orden_deseado:
                # Recorre todos los archivos en la carpeta de entrada
                for archivo in os.listdir(rutaCarpeta):
                    if archivo.lower().endswith('.pdf') and archivo.lower().startswith(prefijo):
                        ruta_archivo = os.path.join(rutaCarpeta, archivo)
                        print(f'Procesando archivo: {ruta_archivo}')
                        
                        # Verifica si el archivo existe
                        if os.path.exists(ruta_archivo):
                            try:
                                # Obtiene el tamaño del archivo en MB
                                archivo_size = os.path.getsize(ruta_archivo) / (1024 * 1024)
                                print(f'Tamaño del archivo: {archivo} es {archivo_size:.2f} MB')

                                # Intentamos abrir el archivo para verificar si está corrupto
                                with open(ruta_archivo, 'rb') as f:
                                    reader = PdfReader(f)  # Se lee el archivo PDF para verificar si es válido
                                    _ = len(reader.pages)  
                                     # Si el archivo es válido, se agrega al merger
                                    print(f'Agregando: {archivo} desde {ruta_archivo}')
                                    merger.append(ruta_archivo)

                               
                                print("Se agregó correctamente!")
                                
                            except (PdfReadError, OSError) as e:
                                # Si hay un error, se registra pero no se detiene el proceso
                                print(f'Error al agregar {archivo}: archivo corrupto o inaccesible ({e})')
                        else:
                            print(f'Archivo no encontrado: {ruta_archivo}')

        # Verifica que haya archivos para combinar antes de escribir el archivo final
        if len(merger.pages) > 0:
            # Escribe el archivo PDF combinado en la ruta de salida
            try:
                with open(ruta_salida, 'wb') as salida_pdf:
                    merger.write(salida_pdf)
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

    
    rutaCarpeta= rutaBase+"\\"+factura

    unirPdf(rutaCarpeta,rutaBase,factura,entidad)

def ComprimirManual(rutaBase,entidad):
    
    # crearCarpeta(rutaBase,"SOPORTES")

    # rutaCarpetaSalida= rutaBase+"\\"+"SOPORTES"

    #Creamos todos los directorios que se encesitan para el guardado de soporets
    crearDirectoriosGuardarSoportes(rutaBase,entidad)
    
    
    #Listamos las carpetas que hay para comprimir
    carpetas = listar_carpetas(rutaBase)

    #Recorremos las carpetas para que usen
    for carpeta in carpetas:
      rutaCarpeta= rutaBase+"\\"+carpeta

      unirPdf(rutaCarpeta,rutaBase,carpeta,entidad)

#Colocar el contrato_armar y la ruta base como parametros de entrada
ruta=sys.argv[1]
contrato_Armar=sys.argv[2]
#ruta= r"C:\Users\YAWI\Desktop\Remision_SS296_1"
#contrato_Armar="SS296"

#ruta=r"C:\Users\YAWI\Downloads\28424"
#contrato_Armar="SS040"
if contrato_Armar in ["SS089","SS040", "SS400", "SS079", "SS457", "SS080", "SS296", "SS401", "SS033"]:
  tipo_armado="1"
elif contrato_Armar in ["SS255"]:
  tipo_armado="2"
elif contrato_Armar in ["SS023", "SS024", "SS022", "SS196", "SS202", "SS390", "SS085", "SS086", "SS482", "SS021", "SS008", "SS009", "SS437", "SS083", "SS458"]:
  tipo_armado="3"
elif contrato_Armar in ["SS019", "SS165", "SS427"]:
  tipo_armado="4"
elif contrato_Armar in ["SS083", "SS458"]:
  tipo_armado="5"
elif contrato_Armar in ["SS208", "SS005", "SS002", "SS004", "SS003", "SS076", "SS171"]:
  tipo_armado="6"
ComprimirManual(ruta,tipo_armado)