#!/usr/bin/env python3
import sys
import math

current_key = None

# Initialiser des variables d'agrégation
sum_load = 0.0
sum_sq = 0.0
count_valid = 0
total = 0

def emit(key, sum_load, sum_sq, count_valid, total):
    if key is None:
        return

    station_id, hour = key

    if count_valid > 0:
        # Calculer la moyenne des load factor
        avg = sum_load / count_valid
        # Calculer la variance
        variance = (sum_sq / count_valid) - (avg ** 2)
        # Calculer l'écart-type en fonction de la variance
        std_load = math.sqrt(max(variance, 0))
    else:
        avg = 0.0
        std_load = 0.0

    print(f"{station_id}\t{hour}\t{avg:.3f}\t{std_load:.3f}\t{count_valid}/{total}")

for line in sys.stdin:
    parts = line.strip().split("\t")
    if len(parts) != 4:
        continue

    station_id, timestamp, load_factor, status_valide = parts

    try:
        timestamp = int(timestamp)
        load = float(load_factor)
        status_valide = int(status_valide)
    except:
        continue

    hour = timestamp // 3600
    key = (station_id, hour)


    
    if current_key != key:        
        # Emettre les résultats agrégés pour le groupe précédent
        emit(current_key, sum_load, sum_sq, count_valid, total)

        # Mettre à jour la clé courante avec la nouvelle clé
        current_key = key

        # Réinitialiser des variables d'agrégation à chaque changement de clé (station_id, hour) pour le nouveau groupe
        sum_load = 0.0
        sum_sq = 0.0
        count_valid = 0
        total = 0

    total += 1

    if status_valide == 1:
	    # Additionner les load factor
        sum_load += load
	    # Additionner les load factor au carré
        sum_sq += load * load
        count_valid += 1

# Emettre les résultats agrégés pour le dernier groupe
emit(current_key, sum_load, sum_sq, count_valid, total)