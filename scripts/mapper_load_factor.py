#!/usr/bin/env python3
from datetime import datetime, timezone
import sys
import json

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue

    try:
        station = json.loads(line)

        station_id = station.get("number")
        
        iso_time = station.get("lastUpdate")

        try:
            dt = datetime.fromisoformat(iso_time.replace("Z", "+00:00"))
            timestamp = int(dt.timestamp())
        except:
            continue

        available_bikes = station.get("totalStands", {}).get("availabilities", {}).get("bikes", 0)
        available_bike_stands = station.get("totalStands", {}).get("availabilities", {}).get("stands", 0)
        status = station.get("status")

        
        if not station_id or not timestamp:
            continue

        # Calculer le load factor
        total = available_bikes + available_bike_stands        

        load_factor = available_bikes / total if total > 0 else 0.0

        # Valider le statut
        status_valide = 1 if (
            status == "OPEN"            
            and 0 <= available_bikes <= available_bike_stands
        ) else 0

        # Sortie (séparateur tabulation)
        print(f"{station_id}\t{timestamp}\t{load_factor:.3f}\t{status_valide}")

    except json.JSONDecodeError:
        continue
    except Exception:
        continue