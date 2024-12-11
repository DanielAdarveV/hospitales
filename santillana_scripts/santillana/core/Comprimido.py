import os
from PyPDF2 import PdfMerger

def unir_pdfs_en_carpeta(carpeta_entrada, carpeta_salida, nombre_factura):
    # Define el orden específico de los archivos
    orden_deseado = ["ekg","hc","epi","ham","oxi","hev","dqx","lab","rx","insumos dqx","hoja gastos", "aplicacion med","auto","electro","anexo","formula","consentimiento","documento","validacion","remision","anestesia","hemod","cardio","traslado","soportes ext","transfusion","insumos rx","gastos urg","gluco","oxigeno","soat","maos","form","consu"]
    
    # Crea una instancia del objeto PdfMerger
    merger = PdfMerger()

    # Recorre el orden deseado y agrega los archivos correspondientes
    for prefijo in orden_deseado:
        # Recorre todos los archivos en la carpeta de entrada

        for archivo in os.listdir(carpeta_entrada):
            if archivo.lower().endswith('.pdf') and archivo.startswith(prefijo):

                ruta_archivo = os.path.join(carpeta_entrada, archivo)
      
                # Agrega el archivo PDF al objeto PdfMerger
                merger.append(ruta_archivo)
                # Imprime el archivo que se está agregando para seguimiento
                print(f'Agregando: {archivo}')

    # Define la ruta del archivo PDF combinado en la carpeta de salida
    ruta_salida = os.path.join(carpeta_salida, f'{nombre_factura}.pdf')

    # Escribe el archivo PDF combinado en la ruta de salida
    merger.write(ruta_salida)
    merger.close()

    print(f'Archivos combinados en: {ruta_salida}')

# Configura la carpeta de entrada, la carpeta de salida y el nombre de la factura
carpeta_entrada = r'Y:\2024\septiembre\Sanitas\Radicado(Remision)\193967'  # Cambia esto a la ruta de tu carpeta de entrada
carpeta_salida = r'Y:\2024\septiembre\Sanitas\SOPORTES'  # Cambia esto a la ruta de tu carpeta de salida
nombre_factura = 'FAC_193967'  # Cambia esto al nombre deseado para el archivo combinado

# Asegúrate de que la carpeta de salida exista, si no, créala
os.makedirs(carpeta_salida, exist_ok=True)

# Llama a la función para unir los PDFs
unir_pdfs_en_carpeta(carpeta_entrada, carpeta_salida, nombre_factura)
