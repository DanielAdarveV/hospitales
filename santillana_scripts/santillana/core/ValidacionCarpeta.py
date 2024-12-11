import os
import datetime
from pathlib import Path
from babel.dates import format_date

# Configurar la localización en español
import locale
#locale.setlocale(locale.LC_ALL, ("es_ES", "UTF-8"))

# Obtener la fecha actual
#fecha_actual = datetime.datetime.now()

# Extraer el año y el mes
#anio_actual = fecha_actual.year

# Obtener el nombre del mes en español usando Babel
#mes_actual = format_date(fecha_actual, format='MMMM', locale='es_ES')

# Construir la ruta base
#ruta_base = Path(f"Y:\\{anio_actual}\\{mes_actual}\\Sanitas\\Remision")

def generar_ruta_carpeta(base_path,plan):
    print(base_path)
    num = 1
    while True: 

        # Construir el nombre de la carpeta con el número adecuado
        nombre_carpeta = "Remision" if num == 0 else f"Remision_{plan}_{num}"
        nueva_ruta = base_path.with_name(nombre_carpeta)
        
        # Si la carpeta no existe, devolver esta ruta
        if not nueva_ruta.exists():
            #return nueva_ruta
            
            os.makedirs(nueva_ruta, exist_ok=True)

            return nueva_ruta
        
        # Incrementar el número para la próxima iteración
        num += 1

    
