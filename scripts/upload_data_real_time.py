from datetime import datetime
import json
from hdfs import InsecureClient
import requests

with open("/run/secrets/api_key") as f:
    API_KEY = f.read().strip()

CONTRACT = "Nantes"

# Récupérer les données en temps réel venant de l'API de JCDecaux
url = f"https://api.jcdecaux.com/vls/v3/stations?contract={CONTRACT}&apiKey={API_KEY}"

client = InsecureClient('http://namenode:9870', user='hadoop')

response = requests.get(url)

if response.status_code == 200:
    data = response.json()   
    
    # Écrire chaque objet de données comme une ligne JSON (JSON Lines) dans un fichier sur HDFS
    with client.write(f'/data-lake/raw/velo_stations/{datetime.now().strftime("%Y-%m-%d-%H")}/data.json', encoding='utf-8', overwrite=True) as writer:
        for station in data:
            line = json.dumps(station, ensure_ascii=False)
            writer.write(line + "\n")

    print(f"✅ Données en temps réel envoyées avec succès dans le fichier 'data.json' stocké dans le répertoire '/data-lake/raw/velo_stations/{datetime.now().strftime('%Y-%m-%d-%H')}' sur HDFS.")

else:
    print(f"Erreur: {response.status_code}")