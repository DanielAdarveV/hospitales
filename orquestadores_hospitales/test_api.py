import requests

#Variables de pruebas
workflow_id = "674f25bd8c90fff5d18a272f"
url = f"https://api.latam.electroneek.com/v1/orchestrator/workflow/{workflow_id}/launch"

payload = { 
    "payload": {
    "idBranch": "1",
    "nameBranch": "Clínica Avidanti Santa Marta",
    "idEps": "1",
    "nameEps": "NUEVA EMPRESA PROMOTORA DE SALUD S.A.",
    "idContract": "1",
    "nameContract": "CASM 2020 - NUEVA EPS",
    "subscriptionType": "CONTRIBUTIVO 2024",
    "executionSegment": "1",
    "ripsDate": "20-10-2024",
    "relationshipNumber": "1"
    }
 }
headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "authorization": "Bearer pG0wkATHI6UOQEWfLqdfjALqo3BhHA7r"
}

response = requests.post(url, json=payload, headers=headers)

print(response.text)