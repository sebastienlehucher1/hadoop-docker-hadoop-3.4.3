#!/usr/bin/env python3
import sys


current_station = None
nb_anomalies = 0
last_anomaly_ts = 0
last_anomaly_type = ""
total_samples = 0 


for line in sys.stdin:
    parts = line.strip().split("\t")
    if len(parts) != 4:
        continue

    station_id, anomaly_type, timestamp, age_last_update = parts

    try:
        anomaly_type = str(anomaly_type)
        timestamp = int(timestamp)      
        


        # Si on passe à une nouvelle station
        if current_station and current_station != station_id:
            # Calculer la fiabilité
            fiabilite = int((total_samples - nb_anomalies) / total_samples * 100) if total_samples else 100
            print(f"{current_station}\t{fiabilite}%\t{nb_anomalies}\t{last_anomaly_type}")

            # Réinitialiser pour la nouvelle station
            nb_anomalies = 0
            last_anomaly_ts = 0
            last_anomaly_type = ""
            total_samples = 0

        current_station = station_id
        nb_anomalies += 1
        total_samples += 1  # Si chaque ligne = 1 échantillon

        # Vérifier si c'est la dernière anomalie
        if timestamp > last_anomaly_ts:
            last_anomaly_ts = timestamp
            last_anomaly_type = anomaly_type
      
    except:
        continue


# Calculer la fiabilité pour la dernière station
if current_station:
    # Si aucune donnée, on évite la division par 0, on considère la fiabilité = 100% par défaut
    fiabilite = int((total_samples - nb_anomalies) / total_samples * 100) if total_samples else 100
    print(f"{current_station}\t{fiabilite}%\t{nb_anomalies}\t{last_anomaly_type}")    