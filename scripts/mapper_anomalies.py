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
        
        last_update = station.get("lastUpdate")

        try:
            last_update_dt = datetime.fromisoformat(last_update.replace("Z", "+00:00"))
            last_update_ts = int(last_update_dt.timestamp())

            now_ts = int(datetime.now(timezone.utc).timestamp())
            age_last_update = now_ts - last_update_ts
        except:
            continue

        available_bikes = station.get("totalStands", {}).get("availabilities", {}).get("bikes", 0)
        available_bike_stands = station.get("totalStands", {}).get("availabilities", {}).get("stands", 0)
        status = station.get("status")

        bike_stands = station.get("totalStands", {}).get("capacity", 0)
        
        if not station_id or not last_update_ts:
            continue

        # Types de dysfonctionnement :

        # Absence de mise à jour depuis plus de 30 min (NO_UPDATE)
        if age_last_update > 1800:
            print(
                f"{station_id}\tNO_UPDATE\t{last_update_ts}\t{age_last_update}"
            )

        # Station ouverte mais vide depuis plus de 2h (ZERO_BIKES)
        if status == "OPEN" and available_bikes == 0 and age_last_update > 7200:
            print(
                f"{station_id}\tZERO_BIKES\t{last_update_ts}\t{age_last_update}"
            )

        # Station systématiquement pleine (FULL_STANDS)
        if available_bike_stands == bike_stands:
            print(
                f"{station_id}\tFULL_STANDS\t{last_update_ts}\t{age_last_update}"
            )

    except json.JSONDecodeError:
        continue
    except Exception:
        continue