def replace_variables(template, variables):
    """Reemplaza las variables en una plantilla de texto."""
    for key, value in variables.items():
        template = template.replace(f'${key}$', str(value))
    return template

def S(src_path, dest_path):
    """Copia un archivo con un contador incremental si ya existe."""
    base, extension = os.path.splitext(dest_path)
    numeracion = 2
    while os.path.exists(dest_path):
        dest_path = f"{base} ({numeracion}){extension}"
        numeracion += 1
    shutil.copy(src_path, dest_path)

def find_and_copy_files(base_path, search_criteria, dest_path_template):
    """Busca archivos según los criterios de búsqueda y los copia al destino."""
    if Path(base_path).is_dir():
        for archivo in os.listdir(base_path):
            if archivo.endswith('.pdf') and any(crit in archivo for crit in search_criteria):
                dest_path = replace_variables(dest_path_template, {'archivo': archivo})
                copy_file_with_counter(os.path.join(base_path, archivo), dest_path)
                return True
    return False

# Variables a usar en el reemplazo
variables = {
    'atencion': atencion,
    'mes_atencion': mes_atencion,
    'nit_entidad': NIT_ENTIDAD,
    'numerofactura': factura,
    'nombre_entidad': entidad,
    'mes_atencion_num': mes_atencion_num,
    'cedula': cedula,
    'fecha_atencion': fecha_atencion,
}

if tipo_nombrado == 'automatizado':
    print("Soporte que ando Buscando", soporte)
    
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

    # Validar existencia y copiar
    if os.path.exists(ruta_completa_buscar):
        ruta_copiar_archivo = os.path.join(ruta_armado, nombre_copia)
        copy_file_with_counter(ruta_completa_buscar, ruta_copiar_archivo)
        soportes_encontrados.append(f"{soporte};{atencion};FA{factura};{tipo_necesidad_soporte}")
        if '$contador$' in datos_json_nomenclatura[fuente]["guardado_armado"][entidad]:
            contadores[id_codificacion] += 1
    elif os.path.exists(ruta_completa_buscar.replace(nombre_a_buscar, nombre_a_buscar.replace(atencion, atencion.replace('-', '_')))):
        ruta_copiar_archivo = os.path.join(ruta_armado, nombre_copia)
        copy_file_with_counter(ruta_completa_buscar.replace(nombre_a_buscar, nombre_a_buscar.replace(atencion, atencion.replace('-', '_'))), ruta_copiar_archivo)
        soportes_encontrados.append(f"{soporte};{atencion};FA{factura};{tipo_necesidad_soporte}")
        if '$contador$' in datos_json_nomenclatura[fuente]["guardado_armado"][entidad]:
            contadores[id_codificacion] += 1
    else:
        if tipo_atencion.__contains__("SU"):
            nombre_a_buscar = nombre_a_buscar.replace(f"{tipo_atencion}-{numero_atencion}", f"{tipo_atencion} - {numero_atencion}")
            ruta_completa_buscar = os.path.join(ruta_soporte, nombre_a_buscar)

            if os.path.exists(ruta_completa_buscar):
                ruta_copiar_archivo = os.path.join(ruta_armado, nombre_copia)
                copy_file_with_counter(ruta_completa_buscar, ruta_copiar_archivo)
                soportes_encontrados.append(f"{soporte};{atencion};FA{factura};{tipo_necesidad_soporte}")
                if '$contador$' in datos_json_nomenclatura[fuente]["guardado_armado"][entidad]:
                    contadores[id_codificacion] += 1
            else:
                soportes_no_encontrados.append(f"{soporte};{atencion};FA{factura};{tipo_necesidad_soporte}")
        else:
            soportes_no_encontrados.append(f"{soporte};{atencion};FA{factura};{tipo_necesidad_soporte}")

# Continuar con la lógica restante de búsqueda y copia de archivos según sea necesario
