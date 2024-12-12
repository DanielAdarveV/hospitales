import unittest
from unittest.mock import patch, mock_open, MagicMock
from santillana.scripts.lecturaJson import EntidadHandler, ProcesadorContratos
import json

class TestEntidadHandler(unittest.TestCase):
    
    @patch("builtins.open", new_callable=mock_open, read_data='{"condiciones": [{"contiene": ["SURA", "LIZA DE"], "entidad_aux": "Sura_poliza_de_salud"}, {"contiene": ["SURA"], "contiene_lower": ["arl"], "entidad_aux": "Sura Arl"}], "default": "default"}')
    def test_cargar_condiciones_desde_json(self, mock_file):
        # Prueba para verificar que las condiciones se cargan correctamente desde el JSON
        handler = EntidadHandler("dummy_path.json")
        self.assertEqual(len(handler.condiciones), 2)
        self.assertEqual(handler.default_entidad, "default")

    def test_determinar_entidad_aux(self):
        # Prueba para verificar la correcta determinación de la entidad auxiliar
        handler = EntidadHandler()
        handler.condiciones = [
            {"contiene": ["SURA", "LIZA DE"], "entidad_aux": "Sura_poliza_de_salud"},
            {"contiene": ["SURA"], "contiene_lower": ["arl"], "entidad_aux": "Sura Arl"}
        ]
        handler.default_entidad = "default"

        entidad1 = "SURA LIZA DE SALUD"
        entidad2 = "sura arl"
        entidad3 = "EPS SANITAS"

        self.assertEqual(handler.determinar_entidad_aux(entidad1), "Sura_poliza_de_salud")
        self.assertEqual(handler.determinar_entidad_aux(entidad2), "Sura Arl")
        self.assertEqual(handler.determinar_entidad_aux(entidad3), "default")


class TestProcesadorContratos(unittest.TestCase):

    @patch("procesador_poo.EntidadHandler")
    @patch("procesador_poo.crearCarpetaArmado")
    def test_procesar_contratos(self, mock_crear_carpeta, MockEntidadHandler):
        # Mock del handler y de la función crearCarpetaArmado
        handler_mock = MockEntidadHandler.return_value
        handler_mock.determinar_entidad_aux.side_effect = lambda entidad: "EntidadMock"

        mock_crear_carpeta.return_value = "ruta_mock"

        datos = [
            {"contrato": "SS201", "entidad": "SURA LIZA DE SALUD"},
            {"contrato": "SS202", "entidad": "EPS SANITAS"}
        ]

        procesador = ProcesadorContratos(datos, "carpeta_json", "carpeta_logs", handler_mock)
        resultado = procesador.procesar_contratos()

        self.assertEqual(len(resultado), 2)
        self.assertEqual(resultado[0]["contrato"], "SS201")
        self.assertEqual(resultado[1]["contrato"], "SS202")
        self.assertEqual(resultado[0]["ruta"], "ruta_mock")
        mock_crear_carpeta.assert_called()
        self.assertEqual(handler_mock.determinar_entidad_aux.call_count, 2)

if __name__ == "__main__":
    unittest.main()
