Q1 — Quelles sont les 15 stations qui n ont plus aucun vélo disponible en ce moment, en commençant par les plus grandes ?


SELECT
    get_json_object(json, '$.number') AS station_id,
    CAST(get_json_object(json, '$.totalStands.availabilities.bikes') AS INT) AS bikes,
    CAST(get_json_object(json, '$.totalStands.capacity') AS INT) AS capacity
FROM raw_velo_stations
WHERE CAST(get_json_object(json, '$.totalStands.availabilities.bikes') AS INT) = 0
ORDER BY capacity DESC
LIMIT 15;