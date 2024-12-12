import json
import requests
from requests.exceptions import RequestException, Timeout
from typing import Any


class APIClient:
    """Clase para interactuar con el servicio API de facturas."""

    BASE_URL = 'https://radicado-santillana.azurewebsites.net/api/v1'

    def __init__(self, timeout: int = 30):
        """
        Inicializa el cliente API.
        
        :param timeout: Tiempo máximo de espera para las solicitudes.
        """
        self.timeout = timeout

    @staticmethod
    def handle_errors(func):
        """
        Decorador para manejar errores en las solicitudes HTTP.
        """
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Timeout:
                print("Error: La solicitud superó el tiempo de espera.")
            except RequestException as e:
                print(f"Error: Ocurrió un problema con la solicitud. Detalle: {e}")
            except ValueError as e:
                print(f"Error: Ocurrió un problema al procesar la respuesta. Detalle: {e}")
            except Exception as e:
                print(f"Error inesperado: {e}")
            return None
        return wrapper

    @handle_errors
    def update_estado_proceso(self, id_reporte: int, estado: str) -> Any:
        """
        Envía una solicitud PUT para actualizar el estado de un reporte.

        :param id_reporte: ID del reporte (PDF).
        :param estado: Estado del proceso a actualizar.
        :return: Respuesta de la API o None en caso de error.
        """
        url = f"{self.BASE_URL}/facturas/estado-proceso"
        payload = {
            "id_reporte": id_reporte,
            "estado_proceso": estado
        }

        headers = {
            "Content-Type": "application/json"
        }

        print(f"Enviando solicitud a {url} con datos: {payload}")

        response = requests.put(url, data=json.dumps(payload), headers=headers, timeout=self.timeout)

        if response.status_code == 200:
            print("Solicitud exitosa:")
            return response.json()
        else:
            print(f"Error en la solicitud. Código de estado: {response.status_code}")
            print(f"Detalle: {response.text}")
            response.raise_for_status()

        return None


if __name__ == "__main__":
    import sys

    # Validación de argumentos al ejecutar el script
    if len(sys.argv) != 2:
        print("Uso: python <script_name>.py <idPDF>")
        sys.exit(1)

    try:
        idPDF_arg = int(sys.argv[1])
    except ValueError:
        print("Error: El argumento idPDF debe ser un número entero.")
        sys.exit(1)

    # Crear instancia del cliente API
    client = APIClient()

    # Llamar al método para actualizar el estado
    response = client.update_estado_proceso(idPDF_arg, "armado_pendiente")

    # Mostrar la respuesta si existe
    if response:
        print(f"Respuesta de la API: {response}")