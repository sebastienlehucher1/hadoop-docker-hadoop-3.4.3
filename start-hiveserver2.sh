#!/bin/bash
set -e

rm -f /opt/hive/conf/hiveserver2.pid

echo "Waiting for HDFS to be ready..."
until hdfs dfs -ls / >/dev/null 2>&1; do
  sleep 3
done

echo "Waiting for NameNode to leave Safe Mode..."
until hdfs dfsadmin -safemode get 2>/dev/null | grep -q "OFF"; do
  sleep 3
done

echo "Deploying Tez into HDFS..."
hdfs dfs -put -f /tez/tez.tar.gz /apps/tez/

echo "Tez deployed successfully."

exec hive \
  --skiphadoopversion \
  --skiphbasecp \
  --service hiveserver2