import json
from pathlib import Path
from santillana_scripts.santillana.scripts.ArmadoFinal import procesar_datos, crearCarpetaArmado
from santillana_scripts.santillana.core.api_client import update_estado_proceso

class EntidadHandler:
    def __init__(self, archivo_json):
        self.entidades_data = self.cargar_json(archivo_json)

    @staticmethod
    def cargar_json(ruta):
        """Carga los datos desde un archivo JSON."""
        with open(ruta, 'r', encoding='utf-8') as file:
            return json.load(file)

    def obtener_entidad_aux(self, entidad):
        """Obtiene la entidad auxiliar en base a las condiciones del JSON."""
        for condicion in self.entidades_data.get("condiciones", []):
            if all(entidad.__contains__(c) for c in condicion.get("contiene", [])) and \
               all(c.lower() in entidad.lower() for c in condicion.get("contiene_lower", [])):
                return condicion["entidad_aux"]

        return self.entidades_data.get("default", "default")


class ProcesadorContratos:
    def __init__(self, carpeta_json, carpeta_logs, archivo_entidades_json):
        self.carpeta_json = carpeta_json
        self.carpeta_logs = carpeta_logs
        self.entidad_handler = EntidadHandler(archivo_entidades_json)
        self.lista_contratos_armar = []

    def procesar_entidades(self, datos):
        """Procesa las entidades y crea carpetas de armado."""
        for item in datos:
            contrato = item.get("contrato")
            entidad = item.get("entidad")

            if not any(d["contrato"] == contrato for d in self.lista_contratos_armar):
                entidad_aux = self.entidad_handler.obtener_entidad_aux(entidad)
                ruta = crearCarpetaArmado(contrato, entidad_aux)
                self.lista_contratos_armar.append({"ruta": ruta, "contrato": contrato})

    def procesar_datos(self, datos):
        """Procesa los datos y ejecuta el script de procesamiento para cada entidad."""
        for item in datos:
            numero_factura = item.get("numero_factura")
            id_reporte = item.get("id_reporte")
            documento = item.get("documento")
            tipo_atencion = item.get("tipo_atencion")
            fecha_ingreso = item.get("fecha_ingreso")
            contrato = item.get("contrato")
            entidad = item.get("entidad").replace("EPS ", "").strip()

            contrato_obj = next((d for d in self.lista_contratos_armar if d["contrato"] == contrato), None)

            if contrato_obj:
                ruta = contrato_obj["ruta"]
                entidad_aux = self.entidad_handler.obtener_entidad_aux(entidad)
                procesar_datos(numero_factura, documento, tipo_atencion, fecha_ingreso, contrato, ruta, entidad, self.carpeta_json, self.carpeta_logs, entidad_aux)
                update_estado_proceso(id_reporte)


if __name__ == "__main__":
    # Configuración de rutas
    carpeta_json = "C:\\Users\\YAWI\\Desktop\\ARMADO\\python"
    carpeta_logs = "C:\\Users\\YAWI\\Desktop\\ARMADO\\Logs\\"
    archivo_json_api = r'C:\\Users\\YAWI\\Desktop\\ARMADO\\JsonApi\\API.json'
    archivo_entidades_json = r'C:\\Users\\YAWI\\Desktop\\ARMADO\\JsonApi\\entidades.json'

    # Cargar datos desde JSON principal
    with open(archivo_json_api, 'r', encoding='utf-8') as file:
        datos = json.load(file)

    # Procesar contratos y entidades
    procesador = ProcesadorContratos(carpeta_json, carpeta_logs, archivo_entidades_json)
    procesador.procesar_entidades(datos)
    procesador.procesar_datos(datos)