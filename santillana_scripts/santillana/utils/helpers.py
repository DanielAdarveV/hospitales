import json
from collections import defaultdict

class Helper:
    def __init__(self,ruta_json,ruta_carpeta_salida):
        self.ruta_json=ruta_json
        self.ruta_carpeta_salida=ruta_carpeta_salida
        self.numero_maquinas = 5
    
    def leer_archivo_json(self,file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
        
    def separar_json(self):

        # Cargar datos desde el archivo
        data = self.leer_archivo_json(self.ruta_json)

        # Crear un diccionario para agrupar por tipo
        result = defaultdict(list)

        # Agrupar elementos por el campo "tipo"
        for item in data:
            tipo = item.get("contrato")
            # tipo = item.get("sigla_sede")
            
            result[tipo].append(item)

        # Imprimir el resultado
        # print(json.dumps(result, indent=4))
        return result

    def dividir_por_maquinas(self):
        data_por_tipo = self.separar_json()
        resultado = {}
        
        # Calcular el total global de objetos
        total_global = sum(len(elementos) for elementos in data_por_tipo.values())
        
        if total_global == 0:
            raise ValueError("No hay datos disponibles para dividir. Verifica los datos de entrada.")
        
        for tipo, elementos in data_por_tipo.items():
            # La cantidad total para este tipo es el número de elementos
            total_cantidad = len(elementos)
            
            # Calcular el número de máquinas asignadas a este tipo
            maquinas = max(1, self.numero_maquinas * total_cantidad // total_global)

            resultado[tipo] = []

            # Distribuir los objetos entre las máquinas
            objetos_por_maquina = total_cantidad // maquinas
            sobrante = total_cantidad % maquinas

            inicio = 0
            for i in range(maquinas):
                # Determinar cuántos objetos asignar a esta máquina
                cantidad_asignada = objetos_por_maquina + (1 if i < sobrante else 0)
                
                if cantidad_asignada > 0:
                    asignacion = elementos[inicio:inicio + cantidad_asignada]
                    inicio += cantidad_asignada

                    # Guardar los resultados
                    for obj in asignacion:
                        asignacion_data = {
                            "id": obj.get("id"),
                            "maquina": i + 1
                        }
                        resultado[tipo].append(asignacion_data)
                    
                    # Crear un archivo por tipo y máquina
                    output_file = f"{self.ruta_carpeta_salida}/{tipo}_maquina_{i + 1}.json"
                    with open(output_file, 'w', encoding='utf-8') as f:
                        json.dump(asignacion, f, ensure_ascii=False, indent=4)
        
        return resultado
    
ruta=r'C:\Users\Usuario\Downloads\lu_lu.json'
ruta_salida=r'C:\Users\Usuario\Documents\GITHUB\hospitales\santillana_scripts\data\processed'
prueba = Helper(ruta,ruta_salida)
resultado_final=prueba.dividir_por_maquinas()
print(json.dumps(resultado_final, indent=4))