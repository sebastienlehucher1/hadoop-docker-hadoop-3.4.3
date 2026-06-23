#!/bin/bash
echo "Initializing HDFS directories..."

# Attendre que le NameNode soit prêt
until hdfs dfs -ls / >/dev/null 2>&1; do
  sleep 3
done

# Attendre la fin du Safe Mode
until hdfs dfsadmin -safemode get 2>/dev/null | grep -q "OFF"; do
  echo "Waiting for NameNode to leave Safe Mode..."
  sleep 3
done

# Créer /apps/tez avec les bonnes permissions
hdfs dfs -mkdir -p /apps/tez
hdfs dfs -chmod 777 /apps/tez

echo "HDFS initialization complete."
