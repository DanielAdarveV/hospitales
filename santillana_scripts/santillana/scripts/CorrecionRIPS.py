import sys
log=[]
# ruta_base="C:\\Users\\Usuario\\Documents\\RIPS\\RAE-119\\"
variables=sys.argv[1]

ruta_base=variables.split('|')[0]
nombre_archivo_base=variables.split('|')[1]
# nombre_archivo_base="XX000119.txt"

nombre_concatenado=ruta_base+nombre_archivo_base

ruta_archivo_ac = nombre_concatenado.replace('XX','AC')
ruta_archivo_am = nombre_concatenado.replace('XX','AM')
ruta_archivo_af = nombre_concatenado.replace('XX','AF')
ruta_archivo_ap = nombre_concatenado.replace('XX','AP')
ruta_archivo_ah = nombre_concatenado.replace('XX','AH')

# print(ruta_archivo_ac)
# print(ruta_archivo_am)
# print(ruta_archivo_af)
# print(ruta_archivo_ap)
# print(ruta_archivo_ah)

tipo_entidad="evento"
diagnosticos_cambiar_am={
    '41072-8':'47006-5',
    '20066836-3':'20066836-1',
    '19935124-4':'19935124-02',
    '19991053-1':'230357-1',
    '20066836-3':	'20066836-1',
    '19947837-1':	'19950452-3',
    '19912860-1':	'19955900-1',
    '38644-5'	:'32513-1',
    '19928399-17':	'19913750-1',
    '19935124-4':'0'	
}


diagnosticos_cambiar_ac = {
    'A09X': 'A090',
    'L89X': 'L890',
    'I845': 'K640',
    'I48X': 'I480',
    'K359': 'K358',
    'H547': 'H549',
    'C850': 'C859',
    'I849': 'K649'
}
mapeodiagnosticos ={}
#-------------------------------------------------------------------------------------------------------------------------------
#CORRECCION ARCHIVO AM
#--------------------------------------------------------------------------------------------------------------

with open(ruta_archivo_am, 'r') as archivo_am:
    lineas_am = archivo_am.readlines()

# Realiza el reemplazo en la posición 14 si es necesario
for i in range(len(lineas_am)):
    # Dividir la línea en campos usando la coma como delimitador
    campos = lineas_am[i].split(',')
    

    #Campo 10 corregir diagnostico
    if len(campos) > 6 and campos[4] != "" and campos[4] in diagnosticos_cambiar_am:
        log.append(f"Se corrije el codigo {campos[4]} con el codigo {diagnosticos_cambiar_am[campos[4]]}")
        print(f"Se corrije el codigo {campos[4]} con el codigo {diagnosticos_cambiar_am[campos[4]]}")
        campos[4]= diagnosticos_cambiar_ac[campos[4]]

        # Reconstruir la línea con los campos modificados
    lineas_am[i] = ','.join(campos)

# Guarda el archivo modificado
with open(ruta_archivo_am, 'w') as archivo_am:
    archivo_am.writelines(lineas_am)

#-------------------------------------------------------------------------------------------------------------------------------
#CORRECCION ARCHIVO AF
#--------------------------------------------------------------------------------------------------------------

with open(ruta_archivo_af, 'r') as archivo_af:
    lineas_af = archivo_af.readlines()

# Realiza el reemplazo en la posición 14 si es necesario
for i in range(len(lineas_af)):
    # Dividir la línea en campos usando la coma como delimitador
    campos = lineas_af[i].split(',')
    

    #Campo 10 corregir diagnostico
    if len(campos) > 13:
        campos[12]="0"
        campos[13]="0"
        campos[14]="0"

        # Reconstruir la línea con los campos modificados
    lineas_af[i] = ','.join(campos)

# Guarda el archivo modificado
with open(ruta_archivo_af, 'w') as archivo_af:
    archivo_af.writelines(lineas_af)


#-------------------------------------------------------------------------------------------------------------------------------
#CORRECCION ARCHIVO AC
#--------------------------------------------------------------------------------------------------------------
with open(ruta_archivo_ac, 'r') as archivo_ac:
    lineas_ac = archivo_ac.readlines()

# Realiza el reemplazo en la posición 14 si es necesario
for i in range(len(lineas_ac)):
    # Dividir la línea en campos usando la coma como delimitador
    campos = lineas_ac[i].split(',')
    
    #Campo 8 siempre debe estar diligenciado -- Cuando el diagn. es por Z, el número debe ser entre 01 y 08, el resto es 10
    if len(campos) > 14 and campos[7]=='':
        
        if campos[9].startswith("Z"):
            
            campos[7]="1"

        else:

            campos[7]="10"

    # Campo 9 siempre debe estar diligenciado -- Cuando es soat es 01 y arl 02, el resto 13
    if len(campos) > 8 and not campos[8].strip():

        if tipo_entidad=="soat":
            campos[8] = "01"
        elif tipo_entidad=="arl":
            campos[8] = "02"
        else:
            campos[8] = "13"

    #Campo 10 siempre debe estar diligenciado--
    if len(campos) > 14 and campos[9] == "":
        log.append(f"No esta diligenciado el diagnostico para la factura {campos[0]} con numero de cedula {campos[3]}")
        print(f"No esta diligenciado el diagnostico para la factura {campos[0]} con numero de cedula {campos[3]}")
    
    #Campo 10 corregir diagnostico
    if len(campos) > 14 and campos[9] != "" and campos[9] in diagnosticos_cambiar_ac:
        log.append(f"Se corrije el codigo {campos[9]} con el codigo {diagnosticos_cambiar_ac[campos[9]]}")
        print(f"Se corrije el codigo {campos[9]} con el codigo {diagnosticos_cambiar_ac[campos[9]]}")
        campos[9]= diagnosticos_cambiar_ac[campos[9]]
    
    if len(campos) > 0: 
        mapeodiagnosticos[campos[0]]=campos[9]

    # Campo 14 siempre debe estar diligenciado -- se debe asignar el valor de 1 
    if len(campos) > 14 and campos[13] == "":
        # Realizar el reemplazo en la posición 14
        campos[13] = "1"    

 
    #Campo 16 siempre permanecer en 0 
    if len(campos) > 15 and campos[15] != "0":
        # Realizar el reemplazo en la posición 14
        campos[15] = "0"
    

        # Reconstruir la línea con los campos modificados
    lineas_ac[i] = ','.join(campos)

# Guarda el archivo modificado
with open(ruta_archivo_ac, 'w') as archivo_ac:
    archivo_ac.writelines(lineas_ac)


#-------------------------------------------------------------------------------------------------------------------------------
#CORRECCION ARCHIVO AF
#--------------------------------------------------------------------------------------------------------------

with open(ruta_archivo_ap, 'r') as archivo_ap:
    lineas_ap = archivo_ap.readlines()

# Realiza el reemplazo en la posición 14 si es necesario
for i in range(len(lineas_ap)):
    # Dividir la línea en campos usando la coma como delimitador
    campos = lineas_ap[i].split(',')
    

    #Campo 10 corregir diagnostico
    if len(campos) > 10 and campos[10]=='' and campos[0] in mapeodiagnosticos:
        campos[10]=mapeodiagnosticos[campos[0]]
        log.append(f'No existia el diagnostico para la factura {campos[0]}, se asigno el del archivo ac {campos[10]}')
        print(f'No existia el diagnostico para la factura {campos[0]}, se asigno el del archivo ac {campos[10]}')

        # Reconstruir la línea con los campos modificados
    lineas_ap[i] = ','.join(campos)

# Guarda el archivo modificado
with open(ruta_archivo_ap, 'w') as archivo_ap:
    archivo_ap.writelines(lineas_ap)



if log!=[""]:
    with open(ruta_base+"Log_RIPS.txt", 'w') as archivo:
        archivo.write("Notas de la correcion de RIPS.\n")

    #Log de 
    
    with open(ruta_base+"Log_RIPS.txt",'r') as f:
             registro_anterior_encontrados=f.read()
             f.close()

    #Concatenamos el texto que habia antes, con el nuevo a agregar
    log.insert(0,registro_anterior_encontrados)
    with open(ruta_base+"Log_RIPS.txt",'w') as f:
            f.write('\n'.join(log))  