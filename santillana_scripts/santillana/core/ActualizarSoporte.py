import json
import requests
import sys



def load_Estados(idPDF):

    url = 'https://radicado-santillana.azurewebsites.net/api/v1/facturas/estado-proceso'

    data = json.dumps(
        {
            "id_reporte": int(idPDF),
            "estado_proceso": "armado_pendiente"
        }
    )
    
    response = requests.put(url, data=data, timeout=30)
    print(response.json())
    # print(response.status_code)

    # try:
    #     print(response.json()["detail"])
    # except TypeError:
    #     print(response.json())

# # * ruta de id del pdf
# idPDF_arg = sys.argv[1]


# load_Estados(idPDF_arg)