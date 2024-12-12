import unittest
from unittest.mock import patch, mock_open, MagicMock
from pathlib import Path
import os
import json
from datetime import datetime
from santillana.scripts.Armado import CarpetaArmado, ProcesadorDatos

class TestCarpetaArmado(unittest.TestCase):

    @patch("folder_processing_poo.datetime")
    @patch("folder_processing_poo.os.makedirs")
    def test_crear_carpeta(self, mock_makedirs, mock_datetime):
        mock_datetime.now.return_value = datetime(2024, 12, 1)
        carpeta = CarpetaArmado(plan="SS400", entidad="Sanitas")
        ruta_esperada = Path("Y:/2024/diciembre/Sanitas/Remision")

        with patch("pathlib.Path.exists", return_value=False):
            ruta_creada = carpeta.crear_carpeta()

        mock_makedirs.assert_called_once_with(ruta_esperada)
        self.assertEqual(ruta_creada, ruta_esperada)

class TestProcesadorDatos(unittest.TestCase):

    @patch("folder_processing_poo.os.path.exists", return_value=True)
    @patch("builtins.open", new_callable=mock_open, read_data='{"key": "value"}')
    def test_cargar_json(self, mock_file, mock_exists):
        ruta_json = "dummy_path.json"
        resultado = ProcesadorDatos.cargar_json(ruta_json)
        self.assertEqual(resultado, {"key": "value"})
        mock_file.assert_called_once_with(ruta_json, 'r', encoding='utf-8')

    @patch("folder_processing_poo.os.path.exists", return_value=False)
    def test_cargar_json_archivo_no_encontrado(self, mock_exists):
        ruta_json = "dummy_path.json"
        with self.assertRaises(FileNotFoundError):
            ProcesadorDatos.cargar_json(ruta_json)

    @patch("folder_processing_poo.shutil.copy")
    @patch("folder_processing_poo.os.path.exists", side_effect=[True, False])
    def test_copiar_archivo(self, mock_exists, mock_copy):
        ProcesadorDatos.copiar_archivo("origen.pdf", "destino.pdf")
        mock_copy.assert_called_once_with("origen.pdf", "destino.pdf")

    @patch("folder_processing_poo.os.path.isdir", return_value=True)
    @patch("folder_processing_poo.os.listdir", return_value=["archivo1.pdf", "archivo2.pdf"])
    @patch("folder_processing_poo.shutil.copy")
    def test_buscar_y_copiar_archivos(self, mock_copy, mock_listdir, mock_isdir):
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

        ruta_origen = "origen"
        nombre_buscar = "archivo"
        ruta_destino = "destino"
        soporte = "soporte"
        tipo_necesidad_soporte = "necesidad"

        resultado = procesador.buscar_y_copiar_archivos(
            ruta_origen, nombre_buscar, ruta_destino, soporte, tipo_necesidad_soporte
        )

        self.assertTrue(resultado)
        mock_copy.assert_called_with(os.path.join(ruta_origen, "archivo1.pdf"), os.path.join(ruta_destino, "archivo1.pdf"))

if __name__ == "__main__":
    unittest.main()