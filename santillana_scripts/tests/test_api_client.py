import unittest
from unittest.mock import patch, MagicMock
from santillana.core.api_client import APIClient  # Asegúrate de usar el nombre real del archivo donde resides el código
from requests.exceptions import Timeout 

class TestAPIClient(unittest.TestCase):

    def setUp(self):
        """Configura el entorno para las pruebas."""
        self.client = APIClient(timeout=10)

    @patch('requests.put')
    def test_update_estado_proceso_success(self, mock_put):
        """Prueba que update_estado_proceso funcione correctamente cuando la API responde exitosamente."""
        # Configurar respuesta simulada de la API
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"detail": "Proceso actualizado exitosamente"}
        mock_put.return_value = mock_response

        # Ejecutar el método
        response = self.client.update_estado_proceso(123, "armado_pendiente")

        # Verificar que se realizó la solicitud correcta
        mock_put.assert_called_once_with(
            "https://radicado-santillana.azurewebsites.net/api/v1/facturas/estado-proceso",
            data='{"id_reporte": 123, "estado_proceso": "armado_pendiente"}',
            headers={"Content-Type": "application/json"},
            timeout=10
        )

        # Verificar la respuesta
        self.assertEqual(response, {"detail": "Proceso actualizado exitosamente"})

    @patch('requests.put')
    def test_update_estado_proceso_failure(self, mock_put):
        """Prueba que update_estado_proceso maneje errores correctamente cuando la API responde con un error."""
        # Configurar respuesta simulada de la API
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.text = "Bad Request"
        mock_put.return_value = mock_response

        # Ejecutar el método y verificar que maneja errores
        response = self.client.update_estado_proceso(123, "estado_invalido")

        # Verificar que la respuesta sea None en caso de error
        self.assertIsNone(response)

    @patch('requests.put', side_effect=Timeout)
    def test_update_estado_proceso_timeout(self, mock_put):
        """Prueba que update_estado_proceso maneje un timeout correctamente."""
        response = self.client.update_estado_proceso(123, "armado_pendiente")
        self.assertIsNone(response)

    @patch('requests.put', side_effect=Exception("Error inesperado"))
    def test_update_estado_proceso_unexpected_error(self, mock_put):
        """Prueba que update_estado_proceso maneje errores inesperados correctamente."""
        response = self.client.update_estado_proceso(123, "armado_pendiente")
        self.assertIsNone(response)


if __name__ == "__main__":
    unittest.main()
