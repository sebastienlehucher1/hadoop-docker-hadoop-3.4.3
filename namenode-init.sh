#!/bin/bash
echo "Initializing HDFS directories..."

# Attendre que le NameNode soit prêt
until hdfs dfs -ls / >/dev/null 2>&1; do
  sleep 3
done

# Attendre la fin du Safe Mode
echo "Waiting for Safe Mode to exit..."

for i in $(seq 1 60); do
  MODE=$(hdfs dfsadmin -safemode get 2>/dev/null || echo "UNKNOWN")

  if echo "$MODE" | grep -q "OFF"; then
    echo "Safe Mode OFF"
    break
  fi

  echo "Still in Safe Mode..."
  sleep 5
done

# Si safemode toujours ON après timeout → on continue quand même
MODE=$(hdfs dfsadmin -safemode get 2>/dev/null || echo "UNKNOWN")
echo "Final SafeMode state: $MODE"


# Créer /apps/tez avec les bonnes permissions
hdfs dfs -mkdir -p /apps/tez
hdfs dfs -chmod 777 /apps/tez

echo "HDFS initialization complete."
