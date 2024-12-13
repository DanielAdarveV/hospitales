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
atencion="URGENCIAS-1"
factura="193536"
documento_paciente="1"
entidad="sanitas"
carpeta_json='C:\\Users\\YAWI\\Desktop\\ARMADO\\python'
carpeta_logs=r'C:\Users\YAWI\Desktop\ARMADO\Prueba\\'
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


#lo recorremos
for fuente in datos_json_soportes[tipo_atencion]:
    
    soportes_por_fuente=datos_json_soportes[tipo_atencion][fuente]
    for tipo_necesidad_soporte in soportes_por_fuente:
        soportes=datos_json_soportes[tipo_atencion][fuente][tipo_necesidad_soporte]
        for soporte in soportes:
         try:
            if fuente!="escaneados":
             tipo_nombrado=datos_json_nomenclatura[fuente]["tipo_nombrado_ruta"]
            else:
             tipo_nombrado=datos_json_nomenclatura[fuente][soporte]["tipo_nombrado_ruta"]
         except:
             print("\n \n\n",datos_json_nomenclatura[fuente])
                
         
         print("---------------------------------------------------------------------")
         if tipo_nombrado == 'automatizado' :     
              
                print("Soporte que ando Buscando",soporte)
                #Obtener el nombre y ruta Esperado a Buscar
                #-----------------------------------------------------------------------------------------------------------------------------------------------
                ruta_soporte=datos_json_nomenclatura[fuente]["ruta"]
                
                #Reemplazamos las posibles variables, para que setee la ruta esperada
                ruta_soporte=ruta_soporte.replace('$atencion$',atencion)
                ruta_soporte=ruta_soporte.replace('$mes_atencion$',mes_atencion)
                ruta_soporte=ruta_soporte.replace('$nit_entidad$',NIT_ENTIDAD)
                ruta_soporte=ruta_soporte.replace('$numerofactura$',factura)
                ruta_soporte=ruta_soporte.replace('$nombre_entidad$',entidad)
                ruta_soporte=ruta_soporte.replace('$mes_atencion_num$',mes_atencion_num)
                ruta_soporte=ruta_soporte.replace('$cedula$',cedula)
                ruta_soporte=ruta_soporte.replace('$fecha_atencion$',fecha_atencion)
                
                #Obtener la Nomenclatura Esperada 
                
                nomenclatura_esperada=datos_json_nomenclatura[fuente]["nomenclatura"]
                
                #Reemplazamos las posibles variables, para qeu setee el nombre mapeado
                nombre_a_buscar=nomenclatura_esperada.replace('$atencion$',atencion)
                nombre_a_buscar=nombre_a_buscar.replace('$numerofactura$',factura)
                nombre_a_buscar=nombre_a_buscar.replace('$soporte$',soporte)
                nombre_a_buscar=nombre_a_buscar.replace('$numerodocumento$',documento_paciente)
                nombre_a_buscar=nombre_a_buscar.replace('$nit_entidad$',NIT_ENTIDAD)
                nombre_a_buscar=nombre_a_buscar.replace('$mes_atencion_num$',mes_atencion_num)
                nombre_a_buscar=nombre_a_buscar.replace('$cedula$',cedula)
                nombre_a_buscar=nombre_a_buscar.replace('$fecha_atencion$',fecha_atencion)
                #Ruta Completa a buscar:
                ruta_completa_buscar=ruta_soporte+"\\"+nombre_a_buscar
                #-----------------------------------------------------------------------------------------------------------------------------------------------
                
                
                #Obtener Nombre que se le va a poner al archivo
                #-----------------------------------------------------------------------------------------------------------------------------------------------
                nombre_copia=datos_json_nomenclatura[fuente]["guardado_armado"][entidad]


                #Replace, para cambiar los datos del nombre_copia es decir con el nombre con el que se guardara el pdf
                nombre_copia=nombre_copia.replace('$atencion$',atencion)
                nombre_copia=nombre_copia.replace('$numerofactura$',factura)
                nombre_copia=nombre_copia.replace('$soporte$',soporte.upper())
                nombre_copia=nombre_copia.replace('$numerodocumento$',documento_paciente)
                nombre_copia=nombre_copia.replace('$nit_entidad$',NIT_ENTIDAD)
                nombre_copia=nombre_copia.replace('$mes_atencion_num$',entidad)
                nombre_copia=nombre_copia.replace('$cedula$',cedula)
                nombre_copia=nombre_copia.replace('$fecha_atencion$',fecha_atencion)

                
                #Validar si Tiene Codificacion
                if nombre_copia.__contains__('$codificacion_entidad$'):
                    id_codificacion=datos_codificacion_entidad[soporte.upper()]
                    nombre_copia=nombre_copia.replace('$codificacion_entidad$',str(id_codificacion))
                    if nombre_copia.__contains__('$contador$') and existe_archivo_codificacion==True:
                        contador=contadores[id_codificacion]
                        nombre_copia=nombre_copia.replace('$contador$',str(contador))
                   
                #-----------------------------------------------------------------------------------------------------------------------------------------------


                #Copiar el Archivo y Agregar a la lista para los  Log de Encontrados o No encontrados    
                #-----------------------------------------------------------------------------------------------------------------------------------------------
                print("ruta en la que lo encontrare",ruta_soporte)
                print("Ruta Con nombre: ",ruta_completa_buscar)
                print("Nombre A Guardar: ",nombre_copia)

                ruta_copiar_archivo=ruta_armado+"\\"+nombre_copia
                print("Segundo nombre ",ruta_completa_buscar.replace(nombre_a_buscar,nombre_a_buscar.replace(atencion,atencion.replace('-','_'))))
                
                contador_sop_exis=2
                #Validamos el Primer nombre que se espera
                if os.path.exists(ruta_completa_buscar):
                    while os.path.exists(ruta_copiar_archivo):
                        base,extension= os.path.splitext(ruta_copiar_archivo)
                        numeracion=2
                        while os.path.exists(f"{base} ({numeracion}){extension}"):
                            numeracion += 1
                        ruta_copiar_archivo=f"{base} ({numeracion}){extension}"
                    shutil.copy(ruta_completa_buscar, ruta_copiar_archivo)
                    soportes_encontrados.append(soporte+";"+atencion+";FA"+factura+";"+tipo_necesidad_soporte)
                    continuar_copia = True 
                    while continuar_copia == True:
                        if os.path.exists(ruta_completa_buscar+" ("+contador_sop_exis+")"):

                            contador_sop_exis=contador_sop_exis+1

                        else:
                            continuar_copia=False
                    
                    if datos_json_nomenclatura[fuente]["guardado_armado"][entidad].__contains__('$contador$'):
                         contadores[id_codificacion]=contadores[id_codificacion]+1

                elif os.path.exists(ruta_completa_buscar.replace(nombre_a_buscar,nombre_a_buscar.replace(atencion,atencion.replace('-','_')))):         
                    while os.path.exists(ruta_copiar_archivo):
                        base,extension= os.path.splitext(ruta_copiar_archivo)
                        numeracion=2
                        while os.path.exists(f"{base} ({numeracion}){extension}"):
                            numeracion += 1
                        ruta_copiar_archivo=f"{base} ({numeracion}){extension}"
                    shutil.copy(ruta_completa_buscar.replace(nombre_a_buscar,nombre_a_buscar.replace(atencion,atencion.replace('-','_'))), ruta_copiar_archivo)
                    soportes_encontrados.append(soporte+";"+atencion+";FA"+factura+";"+tipo_necesidad_soporte)
                    if datos_json_nomenclatura[fuente]["guardado_armado"][entidad].__contains__('$contador$'):
                         contadores[id_codificacion]=contadores[id_codificacion]+1
                else:
                    #Unicamente las SU, viejas tenian una estructura diferente, este else sera innecesario solo debera ir al append De soportes_no_encontrados
                    if tipo_atencion.__contains__("SU"):
                        nombre_a_buscar=nombre_a_buscar.replace(tipo_atencion+"-"+numero_atencion,tipo_atencion+" - "+numero_atencion)
                        ruta_completa_buscar=ruta_soporte+"\\"+nombre_a_buscar

                        if os.path.exists(ruta_completa_buscar):
                            while os.path.exists(ruta_copiar_archivo):
                                base,extension= os.path.splitext(ruta_copiar_archivo)
                                numeracion=2
                                while os.path.exists(f"{base} ({numeracion}){extension}"):
                                    numeracion += 1
                                ruta_copiar_archivo=f"{base} ({numeracion}){extension}"
                            shutil.copy(ruta_completa_buscar, ruta_copiar_archivo)
                            soportes_encontrados.append(soporte+";"+atencion+";FA"+factura+";"+tipo_necesidad_soporte)
                            if datos_json_nomenclatura[fuente]["guardado_armado"][entidad].__contains__('$contador$'):
                                id_codificacion=datos_codificacion_entidad[soporte]
                                contadores[id_codificacion]=contadores[id_codificacion]+1
                        else:
                            soportes_no_encontrados.append(soporte+";"+atencion+";FA"+factura+";"+tipo_necesidad_soporte)
                    else:     
                        soportes_no_encontrados.append(soporte+";"+atencion+";FA"+factura+";"+tipo_necesidad_soporte)
                    
         else:
                encontrado=False
                print("Soporte que ando Buscando",soporte)
                if fuente=='escaneados':
                    ruta_soporte=datos_json_nomenclatura[fuente][soporte]["ruta"]                    
                    nombre_copia=datos_json_nomenclatura[fuente][soporte]["guardado_armado"][entidad]
                else:
                     ruta_soporte=datos_json_nomenclatura[fuente]["ruta"]
                     nombre_copia=datos_json_nomenclatura[fuente]["guardado_armado"][entidad]
                     ruta_soporte=ruta_soporte.replace('$atencion$',atencion)
                print("Ruta de los escaneos: ",ruta_soporte)
                
                #Obtener Nombre que se le va a poner al archivo
                #-----------------------------------------------------------------------------------------------------------------------------------------------
                #nombre_copia=datos_json_nomenclatura[fuente][soporte]["guardado_armado"][entidad]
                nombre_copia=nombre_copia.replace('$atencion$',atencion)
                nombre_copia=nombre_copia.replace('$numerofactura$',factura)
                nombre_copia=nombre_copia.replace('$numerodocumento$',documento_paciente)
                nombre_copia=nombre_copia.replace('$nit_entidad$',NIT_ENTIDAD)
                nombre_factura=nombre_copia.replace('$soporte$',"FA")
                nombre_copia=nombre_copia.replace('$soporte$',soporte.upper())
                nombre_copia=nombre_copia.replace('$cedula$',cedula)
                nombre_copia=nombre_copia.replace('$fecha_atencion$',fecha_atencion)

                if nombre_copia.__contains__('$codificacion_entidad$') and existe_archivo_codificacion==True:
                    id_codificacion=datos_codificacion_entidad[soporte.upper()]
                    nombre_copia=nombre_copia.replace('$codificacion_entidad$',str(id_codificacion))
                    nombre_factura=nombre_copia.replace('$codificacion_entidad$',"OTR")
                    if nombre_copia.__contains__('$contador$') and existe_archivo_codificacion==True:
                        contador=contadores[id_codificacion]
                        nombre_copia=nombre_copia.replace('$contador$',str(contador))
                #-----------------------------------------------------------------------------------------------------------------------------------------------
                #Los escaneos solo buscan que se incluya el nro  y el codigo de la atencion      
                #Recorremos las carpetas
                print("Nombre de la Copia",ruta_soporte)
                
                
                # print("CARPETAS \n \n \n",carpetas)
                
                if soporte!='SE' and soporte!='VD':
                    print("Buscando ",ruta_soporte)
                    if Path(ruta_soporte).is_dir():
                        carpetas=os.listdir(ruta_soporte)
                        for archivo in carpetas:
                            print("Buscando ",)
                            #if os.path.isfile(os.path.join(ruta_soporte,archivo)) and archivo.__contains__(tipo_atencion) and archivo.endswith('.pdf') and archivo.__contains__(numero_atencion) and archivo not in "HA":    
                            if os.path.isfile(os.path.join(ruta_soporte,archivo)) and (archivo.endswith('.pdf') or archivo.endswith('.PDF')) and archivo.lower().__contains__(soporte):
                                print("Encontro")
                                soportes_encontrados.append(soporte+";"+atencion+";FA"+factura+";"+tipo_necesidad_soporte)
                                #soportes_encontrados.append(directorio+"\\"+archivo)
                                ruta_copiar_archivo=ruta_armado+"\\"+nombre_copia

                                while os.path.exists( ruta_copiar_archivo):
                                    base,extension= os.path.splitext(ruta_copiar_archivo)
                                    numeracion=2
                                    while os.path.exists(f"{base} ({numeracion}){extension}"):
                                        numeracion += 1
                                    ruta_copiar_archivo=f"{base} ({numeracion}){extension}"
                                shutil.copy(ruta_soporte+"\\"+archivo, ruta_copiar_archivo)
                                encontrado=True
                                if fuente=='escaneados':
                                    if datos_json_nomenclatura[fuente][soporte]["guardado_armado"][entidad].__contains__('$codificacion_entidad$'):
                                        id_codificacion=datos_codificacion_entidad[soporte]
                                        contadores[id_codificacion]=contadores[id_codificacion]+1
                                else: 
                                    if datos_json_nomenclatura[fuente]["guardado_armado"][entidad].__contains__('$contador$'):
                                        id_codificacion=datos_codificacion_entidad[soporte.upper()]
                                        contadores[id_codificacion]=contadores[id_codificacion]+1
                                break
                        if os.path.exists(ruta_soporte+"\\"+atencion+".pdf")==True:
                            ruta_copiar_archivo= ruta_armado+"\\"+nombre_factura

                            while os.path.exists( ruta_copiar_archivo):
                                    base,extension= os.path.splitext(ruta_copiar_archivo)
                                    numeracion=2
                                    while os.path.exists(f"{base} ({numeracion}){extension}"):
                                        numeracion += 1
                                    ruta_copiar_archivo=f"{base} ({numeracion}){extension}"
                            shutil.copy(ruta_soporte+"\\"+atencion+".pdf",ruta_copiar_archivo)

                    else: 
                        carpetas_no_encontradas.append(ruta_soporte)
                else:
                    if Path(ruta_soporte).is_dir():
                        ruta_carpetas=os.listdir(ruta_soporte)
                        for fichero in ruta_carpetas:
                            directorio=ruta_soporte+"\\"+str(fichero)
                            # print('ARMADO \n \n ',fichero)
                            if os.path.isdir(directorio) == True  and fichero!='AUDITADOS' and fichero!='VERIFICACION DE DERECHOS' :
                            #localFolders=fichero
                                carpetas= os.listdir(directorio)

                                for archivo in carpetas:
                                    #if os.path.isfile(os.path.join(directorio,archivo)) and archivo.__contains__(tipo_atencion) and archivo.endswith('.pdf') and archivo.__contains__(numero_atencion) and archivo not in "HA":
                                    if os.path.isfile(os.path.join(directorio,archivo)) and archivo.__contains__(tipo_atencion) and (archivo.endswith('.pdf') or archivo.endswith('.PDF')) and archivo.__contains__(numero_atencion) and archivo not in "HA":
                                        
                                        soportes_encontrados.append(soporte+";"+atencion+";FA"+factura+";"+tipo_necesidad_soporte)
                                        #soportes_encontrados.append(directorio+"\\"+archivo)
                                        ruta_copiar_archivo= ruta_armado+"\\"+nombre_copia

                                        while os.path.exists( ruta_copiar_archivo):
                                                base,extension= os.path.splitext(ruta_copiar_archivo)
                                                numeracion=2
                                                while os.path.exists(f"{base} ({numeracion}){extension}"):
                                                    numeracion += 1
                                                ruta_copiar_archivo=f"{base} ({numeracion}){extension}"
                                        shutil.copy(directorio+"\\"+archivo, ruta_armado+"\\"+nombre_copia)
                                        encontrado=True
                                        if datos_json_nomenclatura[fuente][soporte]["guardado_armado"][entidad].__contains__('$codificacion_entidad$'):
                                            try:
                                                id_codificacion=datos_codificacion_entidad[soporte.upper()]
                                                # print("IdCodificacion: ",id_codificacion)
                                                contadores[id_codificacion]=contadores[id_codificacion]+1
                                            except:
                                                error="El id no es numero"
                                                # print("El id no es numerico")
                if encontrado==False:
                    soportes_no_encontrados.append(soporte+";"+atencion+";FA"+factura+";"+tipo_necesidad_soporte)  
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