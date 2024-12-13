import sys
import os
import json
import locale
import datetime
import shutil
from pathlib import Path
from pathlib import Path
from babel.dates import format_date

locale.setlocale(locale.LC_ALL, ("es_ES", "UTF-8"))

# Obtener la fecha actual
fecha_actual = datetime.datetime.now()

# Extraer el año y el mes
anio_actual = fecha_actual.year

# Obtener el nombre del mes en español usando Babel
mes_actual = format_date(fecha_actual, format='MMMM', locale='es_ES')

#Variables Principales de Prueba
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
fecha_atencion='20240823'
cedula= "CC1002575853"
atencion="URGENCIAS-PREMIUM"
factura="193967"
documento_paciente="1"
entidad="sanitas"
carpeta_json='C:\\Users\\YAWI\\Desktop\\ARMADO\\python'
carpeta_logs=r'C:\\Users\\YAWI\\Desktop\\ARMADO\Logs\\'
#Ruta del Radicado que estamos manejando
ruta_radicacion=r'C:\Radicacion\Data'
# ruta_armado=r"C:\Users\YAWI\Desktop\ARMADO\Prueba"
ruta_armado = f"Y:\\{anio_actual}\\{mes_actual}\\Sanitas\\Radicado(Remision)\\{factura}"

#ruta_armado="Y:\\2024\\Agosto\\Sanitas\\Radicado(Remision)\\"+factura
# ruta_armado=ruta_radicacion+"\\"+atencion
#-----------------------------------------\----------------------------------------------------------------------------------------------------------------------------------------


#Obtener Variables de Electroneek
# # #---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# fecha_atencion=sys.argv[1]
# atencion=sys.argv[2]
# factura=sys.argv[3]

# documento_paciente=sys.argv[4]
# entidad=sys.argv[5]
# carpeta_json=sys.argv[6]
# carpeta_logs=sys.argv[7]
# #Ruta del Radicado que estamos manejando
# ruta_radicacion=sys.argv[8]
# ruta_armado=sys.argv[9]


#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


#Inicializar y Limpiar Variables 
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
soportes_encontrados=[""]
soportes_no_encontrados=[""]
carpetas_no_encontradas=[""]
#Contadores que se pueden usar para la codificacion de las entidades. Nota: en Venancio se usa para Salud Total
contadores=[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
#Pasamos a minusculas el nombre de la entidad para evitar problemas
entidad=entidad.lower()
print(entidad)
factura=factura.replace('FAC','')
existe_archivo_codificacion=False
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
print(factura)

#Contantes
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
NIT_ENTIDAD="800123106"
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


#Obtencion de Rutas, Creacion de la ruta del armado
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#Ruta del Arhivo Json
archivo_json_soportes=carpeta_json+"\\JsonSoportes.JSON"
archivo_json_nomenclatura=carpeta_json+"\\NomenclaturaSoportes.json"
archivo_json_codificacion_entidad=carpeta_json+"\\"+entidad+".json"

    
#Creamos la carpeta del armado si no existe
if not os.path.exists(ruta_armado):
    os.makedirs(ruta_armado)


#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


#PROCESAMIENTO DE DATOS PARA LA COPIA DE LOS ARCHIVOS
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
tipo_atencion=atencion.split('-')[0]
numero_atencion=atencion.split('-')[1]
#print(tipo_atencion)

#Obtener el mes de la atencion
if fecha_atencion.__contains__('-'):
    convertir_fecha=str(datetime.datetime.strptime(fecha_atencion, "%Y-%m-%d").strftime("%Y-%b-%d")).replace('.','')
    mes_atencion=convertir_fecha.split("-")[1]
else:
    convertir_fecha=str(datetime.datetime.strptime(fecha_atencion, "%Y%m%d").strftime("%Y-%b-%d")).replace('.','')
    mes_atencion=convertir_fecha.split("-")[1]

#Fecha Numerica

if fecha_atencion.__contains__('-'):
    mes_atencion_num=convertir_fecha.split("-")[1]
   
else:
    mes_atencion_num=fecha_atencion[4:6]
    print(mes_atencion_num)

#Se lee el Json Donde esta la relacion de Ruta y nomenclatura del soporte
with open(archivo_json_nomenclatura,'r') as n:
    
    datos_json_nomenclatura=json.load(n)

with open(archivo_json_nomenclatura,'r') as n:
    
    datos_json_nomenclatura=json.load(n)


if os.path.exists(archivo_json_codificacion_entidad):
    
    with open(archivo_json_codificacion_entidad,'r') as n:
        
        datos_codificacion_entidad=json.load(n)
        existe_archivo_codificacion=True
        


#Se lee el Json Donde esta la relacion de Atenciones
with open(archivo_json_soportes,'r') as f:
    
    datos_json_soportes=json.load(f)

#Definicion de funciones 
def replace_variables(template, variables):
    """Reemplaza las variables en una plantilla de texto."""
    for key, value in variables.items():
    
        template = template.replace(f'${key}$', str(value))
    return template

def copy_file_with_counter(src_path, dest_path):
    """Copia un archivo con un contador incremental si ya existe."""
    base, extension = os.path.splitext(dest_path)
    numeracion = 2
    while os.path.exists(dest_path):
        dest_path = f"{base} ({numeracion}){extension}"
        numeracion += 1
    shutil.copy(src_path, dest_path)


def find_and_copy_files(base_path, search_criteria, dest_path_template):
        """Busca todos los archivos según los criterios de búsqueda y los copia al destino."""
        coincidencias = []  # Lista para almacenar todas las coincidencias
        
        if Path(base_path).is_dir():
            for archivo in os.listdir(base_path):
                # Verificar si el archivo cumple con todos los criterios
                matches = [crit for crit in search_criteria if crit in archivo.upper()]
                all_match = all(crit in archivo.upper() for crit in search_criteria)

                # Imprimir el resultado de la evaluación
                # print(f"Evaluando archivo: {archivo}")
                # print(f"Criterios de búsqueda: {search_criteria}")
                # print(f"¿Algún criterio coincide? {'Sí' if all_match else 'No'}")
                # if not matches:
                #     print(f"Criterios que coinciden: {matches}")
                # # else:
                #     print("No hay coincidencias.")


                # Realizar la copia solo si hay coincidencia
                if all_match and archivo.endswith('.pdf'):
                    dest_path = replace_variables(dest_path_template, {'archivo': archivo})
                    copy_file_with_counter(os.path.join(base_path, archivo), dest_path)
                    coincidencias.append(archivo)  # Agregar el archivo coincidente a la lista
        print(coincidencias)
        return coincidencias  # Devolver todas las coincidencias encontradas


# Variables a usar en el reemplazo

soportes_eli=['FAC']
#lo recorremos
for fuente in datos_json_soportes[tipo_atencion]:
    soportes_por_fuente = datos_json_soportes[tipo_atencion][fuente]
    for tipo_necesidad_soporte in soportes_por_fuente:
        soportes = datos_json_soportes[tipo_atencion][fuente][tipo_necesidad_soporte]
        for soporte in soportes:
            
            try:
                if fuente != "escaneados":
                    tipo_nombrado = datos_json_nomenclatura[fuente]["tipo_nombrado_ruta"]
                else:
                    tipo_nombrado = datos_json_nomenclatura[fuente][soporte]["tipo_nombrado_ruta"]
            except:
                print("\n \n\n", datos_json_nomenclatura[fuente])

            print("---------------------------------------------------------------------")
            variables = {
                'atencion': atencion,
                'mes_atencion': mes_atencion,
                'nit_entidad': NIT_ENTIDAD,
                'numerofactura': factura,
                'nombre_entidad': entidad,
                'mes_atencion_num': mes_atencion_num,
                'cedula': cedula,
                'fecha_atencion': fecha_atencion,
                'soporte': soporte.upper(),
            }

            if tipo_nombrado == 'automatizado':
                print("Soporte que ando buscando", soporte)
                
                # Obtener la ruta y nomenclatura esperada
                ruta_soporte = replace_variables(datos_json_nomenclatura[fuente]["ruta"], variables)
                nomenclatura_esperada = datos_json_nomenclatura[fuente]["nomenclatura"]
                nombre_a_buscar = replace_variables(nomenclatura_esperada, variables)

                ruta_completa_buscar = os.path.join(ruta_soporte, nombre_a_buscar)

                # Preparar el nombre de copia
                nombre_copia = replace_variables(datos_json_nomenclatura[fuente]["guardado_armado"][entidad], variables)
                
                # Validar si tiene codificación
                if '$codificacion_entidad$' in nombre_copia:
                    id_codificacion = datos_codificacion_entidad[soporte.upper()]
                    nombre_copia = nombre_copia.replace('$codificacion_entidad$', str(id_codificacion))
                    if '$contador$' in nombre_copia and existe_archivo_codificacion:
                        nombre_copia = nombre_copia.replace('$contador$', str(contadores[id_codificacion]))

                # Mostrar información
                print("Ruta en la que lo encontraré", ruta_soporte)
                print("Ruta con nombre:", ruta_completa_buscar)
                print("Nombre a guardar:", nombre_copia)

                # Usar find_and_copy_files para buscar y copiar
                if find_and_copy_files(ruta_soporte, [nombre_a_buscar.replace('.pdf','')], os.path.join(ruta_armado, nombre_copia)):
                    soportes_encontrados.append(f"{soporte};{atencion};FA{factura};{tipo_necesidad_soporte}")
                    if '$contador$' in datos_json_nomenclatura[fuente]["guardado_armado"][entidad]:
                        contadores[id_codificacion] += 1
                else:
                    # Lógica adicional para tratar casos especiales si find_and_copy_files no encuentra el archivo
                    soportes_no_encontrados.append(f"{soporte};{atencion};FA{factura};{tipo_necesidad_soporte}")
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Verificar y crear el archivo de log si no existe
log_no_encontrados_path = os.path.join(carpeta_logs, "LogNoEncontrados.txt")
if not os.path.exists(log_no_encontrados_path):
    open(log_no_encontrados_path, 'w').close()

#Guardar los Logs de lo Que no se encontro 
if soportes_no_encontrados != [""]:
    with open(log_no_encontrados_path, 'r') as f:
        registro_anterior_no_encontrados = f.read()
    soportes_no_encontrados.insert(0, registro_anterior_no_encontrados)
    with open(log_no_encontrados_path, 'w') as f:
        f.write('\n'.join(soportes_no_encontrados))

# Verificar y crear el archivo de log si no existe
log_encontrados_path = os.path.join(carpeta_logs, "LogEncontrados.txt")
if not os.path.exists(log_encontrados_path):
    open(log_encontrados_path, 'w').close()

#Guardar los Logs de lo Que se encontro 
if soportes_encontrados != [""]:
    with open(log_encontrados_path, 'r') as f:
        registro_anterior_encontrados = f.read()
    soportes_encontrados.insert(0, registro_anterior_encontrados)
    with open(log_encontrados_path, 'w') as f:
        f.write('\n'.join(soportes_encontrados))

# Verificar y crear el archivo de log si no existe
log_sin_carpeta_path = os.path.join(carpeta_logs, "LogSinCarpeta.txt")
if not os.path.exists(log_sin_carpeta_path):
    open(log_sin_carpeta_path, 'w').close()

#Guardar los Logs de carpetas no encontradas
if carpetas_no_encontradas != [""]:
    with open(log_sin_carpeta_path, 'r') as f:
        registro_anterior_no_encontradas = f.read()
    carpetas_no_encontradas.insert(0, registro_anterior_no_encontradas)
    with open(log_sin_carpeta_path, 'w') as f:
        f.write('\n'.join(carpetas_no_encontradas))

#Guardar los Logs de lo Que no se encontro 
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#Validamos si la variable no esta vacia, con el fin de que no queden espacios en el log
if soportes_no_encontrados!=[""]:
    #Leemos el archivo
    with open(carpeta_logs+"\\"+"LogNoEncontrados.txt",'r') as f:
             registro_anterior_no_encontrados=f.read()
             f.close()
    #Concatenamos el texto que habia antes, con el nuevo a agregar
    soportes_no_encontrados.insert(0,registro_anterior_no_encontrados)
    with open(carpeta_logs+"\\"+"LogNoEncontrados.txt",'w') as f:
            f.write('\n'.join(soportes_no_encontrados))   

#Validamos si la variable no esta vacia, con el fin de que no queden espacios en el log
if soportes_encontrados!=[""]:
    #Log de los archivos Encontrados
    with open(carpeta_logs+"\\"+"LogEncontrados.txt",'r') as f:
             registro_anterior_encontrados=f.read()
             f.close()
    #Concatenamos el texto que habia antes, con el nuevo a agregar
    soportes_encontrados.insert(0,registro_anterior_encontrados)
    with open(carpeta_logs+"\\"+"LogEncontrados.txt",'w') as f:
            f.write('\n'.join(soportes_encontrados))    

if  carpetas_no_encontradas!=[""]:
    #Log de los archivos Encontrados
    with open(carpeta_logs+"\\"+"LogSinCarpeta.txt",'r') as f:
             registro_anterior_encontrados=f.read()
             f.close()
    #Concatenamos el texto que habia antes, con el nuevo a agregar
    carpetas_no_encontradas.insert(0,registro_anterior_encontrados)
    with open(carpeta_logs+"\\"+"LogSinCarpeta.txt",'w') as f:
            f.write('\n'.join( carpetas_no_encontradas))    
            
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------