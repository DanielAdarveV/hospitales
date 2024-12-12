import os
import json
import locale
import datetime
import shutil
from pathlib import Path
from babel.dates import format_date

class CarpetaArmado:
    def __init__(self, plan, entidad):
        self.plan = plan
        
        self.entidad = entidad
        self.ruta_carpeta = self.generar_ruta_carpeta()

    def generar_ruta_carpeta(self):
        """Genera la ruta de la carpeta basado en el año y el mes actual."""
        locale.setlocale(locale.LC_ALL, ("es_ES", "UTF-8"))
        fecha_actual = datetime.datetime.now()
        anio_actual = fecha_actual.year
        mes_actual = format_date(fecha_actual, format='MMMM', locale='es_ES')
        ruta_base = Path(f"Y:\\{anio_actual}\\{mes_actual}\\{self.entidad}\\Remision")
        return ruta_base

    def crear_carpeta(self):
        """Crea la carpeta en la ruta especificada si no existe."""
        if not self.ruta_carpeta.exists():
            os.makedirs(self.ruta_carpeta)
        return self.ruta_carpeta


class ProcesadorDatos:
    def __init__(self, factura, cedula, atencion, fecha_atencion, contrato, carpeta_json, carpeta_logs, entidad, entidad_aux):
        self.factura = factura.replace('FAC', '')
        self.cedula = cedula
        self.atencion = atencion or "HOSPITALZADO"
        self.fecha_atencion = fecha_atencion.replace('-', '')
        self.contrato = contrato
        self.carpeta_json = carpeta_json
        self.carpeta_logs = carpeta_logs
        self.entidad = entidad.lower()
        self.entidad_aux = entidad_aux.lower()
        self.contadores = [1] * 18
        self.planes_premium = ["SS400"]
        self.tipo_atencion = self.obtener_tipo_atencion()
        self.nit_entidad = "800123106"

        # Listas para registrar soportes
        self.soportes_encontrados = []
        self.soportes_no_encontrados = []

        # Rutas de los JSON
        self.archivo_json_soportes = os.path.join(carpeta_json, "JsonSoportes.JSON")
        self.archivo_json_nomenclatura = os.path.join(carpeta_json, "NomenclaturaSoportes.json")
        self.archivo_json_codificacion_entidad = os.path.join(carpeta_json, f"{self.entidad}.json")

        # Datos cargados desde los JSON
        self.datos_json_soportes = self.cargar_json(self.archivo_json_soportes)
        self.datos_json_nomenclatura = self.cargar_json(self.archivo_json_nomenclatura)
        self.datos_codificacion_entidad = self.cargar_json(self.archivo_json_codificacion_entidad, obligatorio=False)

    def obtener_tipo_atencion(self):
        """Determina el tipo de atención basándose en el contrato."""
        tipo_atencion = self.atencion.split('-')[0]
        if self.contrato in self.planes_premium:
            tipo_atencion += "-PREMIUM"
        else:
            tipo_atencion += "-NORMAL"
        return tipo_atencion

    @staticmethod
    def cargar_json(ruta, obligatorio=True):
        """Carga un archivo JSON desde la ruta especificada."""
        if os.path.exists(ruta):
            with open(ruta, 'r', encoding='utf-8') as archivo:
                return json.load(archivo)
        elif obligatorio:
            raise FileNotFoundError(f"El archivo JSON no se encontró: {ruta}")
        return {}

    @staticmethod
    def reemplazar_variables(template, variables):
        """Reemplaza las variables en una plantilla de texto."""
        for key, value in variables.items():
            template = template.replace(f'${key}$', str(value))
        return template

    @staticmethod
    def copiar_archivo(src_path, dest_path):
        """Copia un archivo al destino, evitando sobrescribirlo."""
        base, extension = os.path.splitext(dest_path)
        contador = 2
        while os.path.exists(dest_path):
            dest_path = f"{base} ({contador}){extension}"
            contador += 1
        shutil.copy(src_path, dest_path)

    def procesar_datos(self, carpeta_armado):
        """Procesa los datos y organiza los soportes."""
        ruta_armado = os.path.join(carpeta_armado, self.factura)
        if not os.path.exists(ruta_armado):
            os.makedirs(ruta_armado)

        for fuente, soportes_por_fuente in self.datos_json_soportes[self.tipo_atencion].items():
            nomenclatura_fuente = self.datos_json_nomenclatura.get(fuente, {})

            for tipo_necesidad_soporte, soportes in soportes_por_fuente.items():
                for soporte in soportes:
                    self.procesar_soporte(fuente, soporte, tipo_necesidad_soporte, nomenclatura_fuente, ruta_armado)

    def procesar_soporte(self, fuente, soporte, tipo_necesidad_soporte, nomenclatura_fuente, ruta_armado):
        """Procesa cada soporte según su tipo."""
        variables = {
            'atencion': self.atencion,
            'mes_atencion': self.fecha_atencion[4:6],
            'nit_entidad': self.nit_entidad,
            'numerofactura': self.factura,
            'nombre_entidad': self.entidad,
            'nombre_entidad_aux': self.entidad_aux,
            'cedula': self.cedula,
            'fecha_atencion': self.fecha_atencion,
            'soporte': soporte.upper(),
        }

        if fuente != "escaneados":
            tipo_nombrado = nomenclatura_fuente.get("tipo_nombrado_ruta")
        else:
            tipo_nombrado = nomenclatura_fuente.get(soporte, {}).get("tipo_nombrado_ruta")

        if tipo_nombrado == 'automatizado':
            ruta_soporte = self.reemplazar_variables(nomenclatura_fuente.get("ruta", ""), variables)
            nomenclatura_esperada = self.reemplazar_variables(nomenclatura_fuente.get("nomenclatura", ""), variables)

            if self.buscar_y_copiar_archivos(ruta_soporte, nomenclatura_esperada, ruta_armado, soporte, tipo_necesidad_soporte):
                self.soportes_encontrados.append(f"{soporte};{self.atencion};FA{self.factura};{tipo_necesidad_soporte}")
            else:
                self.soportes_no_encontrados.append(f"{soporte};{self.atencion};FA{self.factura};{tipo_necesidad_soporte}")

    def buscar_y_copiar_archivos(self, ruta_origen, nombre_buscar, ruta_destino, soporte, tipo_necesidad_soporte):
        """Busca y copia archivos desde una ruta origen al destino."""
        if not os.path.isdir(ruta_origen):
            return False

        archivos_encontrados = False
        for archivo in os.listdir(ruta_origen):
            if archivo.upper().startswith(nombre_buscar.upper()) and archivo.endswith('.pdf'):
                dest_path = os.path.join(ruta_destino, archivo)
                self.copiar_archivo(os.path.join(ruta_origen, archivo), dest_path)
                archivos_encontrados = True

        return archivos_encontrados


# Ejecución del script
if __name__ == "__main__":
    # Instancia de la clase CarpetaArmado
    carpeta = CarpetaArmado(plan="SS400", entidad="Sanitas")
    ruta_carpeta = carpeta.crear_carpeta()

    # Instancia de la clase ProcesadorDatos
    procesador = ProcesadorDatos(
        factura="FAC123456",
        cedula="CC1234567890",
        atencion="HOSPITALIZADO",
        fecha_atencion="2024-08-23",
        contrato="SS400",
        carpeta_json="C:\\Users\\Jsons",
        carpeta_logs="C:\\Users\\Logs",
        entidad="Sanitas",
        entidad_aux="Sanitas Aux"
    )

    # Procesar datos
    procesador.procesar_datos(ruta_carpeta)