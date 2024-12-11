import sys
import os
import json
import locale
import datetime
import shutil
from pathlib import Path
from pathlib import Path
from babel.dates import format_date
from ValidacionCarpeta import generar_ruta_carpeta

def crearCarpetaArmado(plan,entidad):
    locale.setlocale(locale.LC_ALL, ("es_ES", "UTF-8"))

    # Obtener la fecha actual
    fecha_actual = datetime.datetime.now()

    # Extraer el año y el mes
    anio_actual = fecha_actual.year

    # Obtener el nombre del mes en español usando Babel
    mes_actual = format_date(fecha_actual, format='MMMM', locale='es_ES')
    ruta_base = Path(f"Y:\\{anio_actual}\\{mes_actual}\\{entidad}\\Remision")
    nueva_carpeta = generar_ruta_carpeta(ruta_base,plan)
    #os.makedirs(nueva_carpeta)
   
    return nueva_carpeta

def procesar_datos(factura,cedula,atencion,fecha_atencion,contrato,nueva_carpeta,entidad_guardado_armado,carpeta_json,carpeta_logs,entidad_aux):

    locale.setlocale(locale.LC_ALL, ("es_ES", "UTF-8"))
    print(entidad_guardado_armado)


    # if entidad.__contains__("SURA"):
    #     entidad="sura"
    # elif entidad.__contains__("SANITAS"):
    #     entidad="Sanitas"
    print(f"2-{entidad_guardado_armado}")
    #Variables Principales de Prueba
    #---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # fecha_atencion='20240823'
    planes_premium=["SS400"]
    # cedula= "CC24308706"
    # contrato="SS040"
    # atencion="HOSPITALZADO"
    # factura="197074"
    # fecha_atencion= "2024-08-08"

    # factura="195085"

    # factura=sys.argv[1]
    # cedula= sys.argv[2]
    # atencion=sys.argv[3]
    # fecha_atencion= sys.argv[4]
    # contrato=sys.argv[5]

    #Limpiar Fecha
    fecha_atencion=fecha_atencion.replace('-','')
   
    #documento_paciente="1"
    #entidad="Sanitas"
    #carpeta_json='C:\\Users\\YAWI\\Desktop\\ARMADO\\python'
    #carpeta_logs=r'C:\\Users\\YAWI\\Desktop\\ARMADO\\Logs\\'
    #Ruta del Radicado que estamos manejando
    ruta_radicacion=r'C:\Radicacion\Data'
    # ruta_armado=r"C:\Users\YAWI\Desktop\ARMADO\Prueba"
    # Definir la ruta base para la carpeta `Remision`
    ruta_armado = f"{nueva_carpeta}\\{factura}"

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
    entidad_guardado_armado=entidad_guardado_armado.lower()
    # print(entidad)
    factura=factura.replace('FAC','')
    existe_archivo_codificacion=False
    #---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # print(factura)

    #Contantes
    #---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    NIT_ENTIDAD="800123106"
    #---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


    #Obtencion de Rutas, Creacion de la ruta del armado
    #---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #Ruta del Arhivo Json
    archivo_json_soportes=carpeta_json+"\\JsonSoportes.JSON"
    archivo_json_nomenclatura=carpeta_json+"\\NomenclaturaSoportes.json"
    archivo_json_codificacion_entidad=carpeta_json+"\\"+entidad_guardado_armado+".json"

        
    #Creamos la carpeta del armado si no existe
    if not os.path.exists(ruta_armado):
        os.makedirs(ruta_armado)


    #---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


    #PROCESAMIENTO DE DATOS PARA LA COPIA DE LOS ARCHIVOS
    #---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    if atencion is None or atencion =="null":
        atencion="HOSPITALZADO"
    tipo_atencion=atencion.split('-')[0]



    if contrato in planes_premium:
        tipo_atencion=tipo_atencion+"-"+"PREMIUM"
    else:
        tipo_atencion=tipo_atencion+"-"+"NORMAL"
    # numero_atencion=atencion.split('-')[1]
    print(tipo_atencion)

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
        # print(mes_atencion_num)

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
        
        # Convertimos los criterios a mayúsculas una sola vez para evitar conversiones repetitivas
        search_criteria = [crit.upper() for crit in search_criteria]

        if Path(base_path).is_dir():
            for archivo in os.listdir(base_path):
                archivo_upper = archivo.upper()  # Convertir el nombre del archivo a mayúsculas una vez
                
                # Filtrar solo los archivos PDF
                if not archivo.endswith('.pdf'):
                    continue
                
                # Verificar si el archivo cumple con todos los criterios
                if all(crit in archivo_upper for crit in search_criteria):
                    # Solo construir la ruta de destino si se cumple la condición
                    dest_path = replace_variables(dest_path_template, {'archivo': archivo})
                    copy_file_with_counter(os.path.join(base_path, archivo), dest_path)
                    coincidencias.append(archivo)  # Agregar el archivo coincidente a la lista
                    
        # print(coincidencias)
        return coincidencias  # Devolver todas las coincidencias encontradas


    # Variables a usar en el reemplazo
    for fuente, soportes_por_fuente in datos_json_soportes[tipo_atencion].items():
        # Accedemos solo una vez a la nomenclatura de la fuente
        nomenclatura_fuente = datos_json_nomenclatura.get(fuente, {})
        
        for tipo_necesidad_soporte, soportes in soportes_por_fuente.items():
            for soporte in soportes:
                try:
                    # Determinar el tipo_nombrado basándonos en si la fuente es "escaneados"
                    if fuente != "escaneados":
                        tipo_nombrado = nomenclatura_fuente.get("tipo_nombrado_ruta")
                    else:
                        tipo_nombrado = nomenclatura_fuente.get(soporte, {}).get("tipo_nombrado_ruta")
                except KeyError:
                    # print(f"Error al obtener nomenclatura para fuente: {fuente}")
                    continue

                # print("---------------------------------------------------------------------")
                variables = {
                    'atencion': atencion,
                    'mes_atencion': mes_atencion,
                    'nit_entidad': NIT_ENTIDAD,
                    'numerofactura': factura,
                    'nombre_entidad': entidad_guardado_armado,
                    'nombre_entidad_aux': entidad_aux,
                    'mes_atencion_num': mes_atencion_num,
                    'cedula': cedula,
                    'fecha_atencion': fecha_atencion,
                    'soporte': soporte.upper(),
                }

                if tipo_nombrado == 'automatizado':
                    # print(f"Soporte que estoy buscando: {soporte}")

                    # Obtener la ruta y nomenclatura esperada
                    ruta_soporte = replace_variables(nomenclatura_fuente.get("ruta", ""), variables)
                    nomenclatura_esperada = nomenclatura_fuente.get("nomenclatura", "")
                    nombre_a_buscar = replace_variables(nomenclatura_esperada, variables)
                    
                    ruta_completa_buscar = os.path.join(ruta_soporte, nombre_a_buscar)

                    # Preparar el nombre de copia
                    nombre_copia = replace_variables(
                        nomenclatura_fuente.get("guardado_armado", {}).get(entidad_guardado_armado, ""), 
                        variables
                    )

                    # Validar si tiene codificación
                    if '$codificacion_entidad$' in nombre_copia:
                        id_codificacion = datos_codificacion_entidad.get(soporte.upper(), "")
                        nombre_copia = nombre_copia.replace('$codificacion_entidad$', str(id_codificacion))
                        
                        if '$contador$' in nombre_copia and existe_archivo_codificacion:
                            nombre_copia = nombre_copia.replace('$contador$', str(contadores[id_codificacion]))

                    # Mostrar información solo si es necesario
                    # print(f"Ruta en la que lo encontraré: {ruta_soporte}")
                    # print(f"Ruta con nombre: {ruta_completa_buscar}")
                    # print(f"Nombre a guardar: {nombre_copia}")

                    # Usar find_and_copy_files para buscar y copiar
                    if find_and_copy_files(ruta_soporte, [nombre_a_buscar.replace('.pdf', '')], os.path.join(ruta_armado, nombre_copia)):
                        soportes_encontrados.append(f"{soporte};{atencion};FA{factura};{tipo_necesidad_soporte}")
                        if '$contador$' in nomenclatura_fuente.get("guardado_armado", {}).get(entidad_guardado_armado, ""):
                            contadores[id_codificacion] += 1
                    else:
                        # Lógica adicional para tratar casos especiales si no encuentra el archivo
                        soportes_no_encontrados.append(f"{soporte};{atencion};FA{factura};{tipo_necesidad_soporte}")
