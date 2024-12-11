from ArmadoFinal import procesar_datos
from ActualizarSoporte import load_Estados
from ArmadoFinal import crearCarpetaArmado
import sys
import json
#from ComprimidoFinal import ComprimirEndPoint
#from ComprimidoFinal import ComprimirManual
#from ComprimidoFinal import crearCarpeta

# Nombre del archivo JSON

#archivo_json=sys.argv[1]
#carpeta_json=sys.argv[2]
#carpeta_logs=sys.argv[3]

carpeta_json="C:\\Users\\YAWI\\Desktop\\ARMADO\\python"
carpeta_logs="C:\\Users\\YAWI\\Desktop\\ARMADO\\Logs\\"
archivo_json = r'C:\Users\YAWI\Desktop\ARMADO\JsonApi\API.json'


if isinstance(carpeta_json, tuple):
    carpeta_json = carpeta_json[0]

with open(archivo_json, 'r') as file:
    datos = json.load(file)


lista_contratos_armar = []
for item in datos:
    contrato = item.get('contrato')
    entidad = item.get('entidad')

    armados_particulares= []
    if entidad in armados_particulares:
        print("posee un armado particular")
    else:
        
        if entidad.__contains__("SURA") and entidad.__contains__("LIZA DE"):
            entidad_aux="Sura_poliza_de_salud"
        elif  entidad.__contains__("SURA") and entidad.lower().__contains__("arl"):
                entidad_aux='Sura Arl'
        elif entidad == "EPS SANITAS":
                entidad_aux="Sanitas"
        elif entidad.__contains__("COOMEVA"):
                entidad_aux="Coomeva"
        elif entidad.__contains__("COLSANITAS"):
                entidad_aux="Colsanitas"
        elif entidad.__contains__("COLPATRIA SOAT"):
                entidad_aux="axa_colpatria_soat"
        elif entidad.__contains__("AXA COLPATRIA ARL"):
                entidad_aux="axa_colpatria_arl"
        elif entidad.__contains__("SEGUROS BOLIVAR"):
                entidad_aux="seguros_bolivar_soat"
        elif entidad.__contains__("POSITIVA ARL"):
                entidad_aux="Positiva Arl"
        elif entidad.__contains__("ALLIANZ"):
                entidad_aux="allianz_allianz_medical"
        elif entidad.__contains__("COLMENA ARL"):
                entidad_aux="colmena_arl"

        entidad="default"
         
    
   
        
    # Llamar al segundo script con los datos como argumentos
    if not any(d['contrato'] ==contrato  for d in lista_contratos_armar):
        ruta=crearCarpetaArmado(contrato,entidad_aux)
        lista_contratos_armar.append({'ruta':ruta,'contrato':contrato})
print(lista_contratos_armar)

#rutaBase=r"Y:\2024\septiembre\Sanitas\Remision"
#ComprimirManual(rutaBase,contrato_Armar)

for item in datos:
    numero_factura = item.get('numero_factura')
    id_reporte = item.get('id_reporte')
    documento = item.get('documento')
    tipo_atencion = item.get('tipo_atencion')
    fecha_ingreso = item.get('fecha_ingreso')
    contrato = item.get('contrato')
    entidad = item.get('entidad')
    entidad = entidad.replace("EPS ", "").strip()
        # Llamar al segundo script con los datos como argumentos
    
    # if  any(d['contrato'] ==contrato  for d in lista_contratos_armar):
    contrato_obj = next((d for d in lista_contratos_armar if d['contrato']==contrato),None)   

    if contrato_obj: 
        ruta=contrato_obj['ruta']
        # print(ruta)

        #Limpieza entidad 
        armados_particulares= []
        if entidad in armados_particulares:
            print("posee un armado particular")
        else:
            
            if entidad.__contains__("SURA") and entidad.__contains__("LIZA DE"):
                entidad_aux="Sura_poliza_de_salud"
            elif  entidad.__contains__("SURA") and entidad.lower().__contains__("arl"):
                    entidad_aux='Sura Arl'
            elif entidad == "EPS SANITAS":
                    entidad_aux="Sanitas"
            elif entidad.__contains__("COOMEVA"):
                    entidad_aux="Coomeva"
            elif entidad.__contains__("COLSANITAS"):
                    entidad_aux="Colsanitas"
            elif entidad.__contains__("COLPATRIA SOAT"):
                    entidad_aux="Colpatria Soat"
            elif entidad.__contains__("AXA COLPATRIA ARL"):
                    entidad_aux="axa_colpatria_arl"
            elif entidad.__contains__("SEGUROS BOLIVAR"):
                    entidad_aux="seguros_bolivar_soat"
            elif entidad.__contains__("POSITIVA ARL"):
                    entidad_aux="Positiva Arl"
            elif entidad.__contains__("ALLIANZ"):
                    entidad_aux="allianz_allianz_medical"
            elif entidad.__contains__("COLMENA ARL"):
                    entidad_aux="colmena_arl"

            entidad="default"
            
        # print(entidad)

        procesar_datos(numero_factura, documento, tipo_atencion, fecha_ingreso, contrato, ruta, entidad, carpeta_json, carpeta_logs,entidad_aux)
        load_Estados(id_reporte)   
         

   #rutaBase=r"Y:\2024\septiembre\Sanitas\Remision"
            # ComprimirEndPoint(rutaBase,numero_factura,contrato)
        
            # load_Estados(id_reporte)


    
# # Extraer los campos requeridos


