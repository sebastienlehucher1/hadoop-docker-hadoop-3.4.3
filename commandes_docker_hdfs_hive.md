## Commandes Docker :
```
Exécuter le script 'Data_Real_Time.py' dans le conteneur namenode :
docker exec -it namenode python /opt/hadoop/scripts/upload_data_real_time.py

Accéder à la base de données metastore_db dans le conteneur metastore-db :
docker exec -it metastore-db psql -U hive -d metastore_db
```

## Commandes SQL dans la base de données metastore_db :
```
Réinitialiser complètement le schéma :
DROP SCHEMA public CASCADE;
CREATE SCHEMA public;
```

## Commandes hdfs :
```
hdfs dfs -ls -R /data-lake/raw/velo_stations/ \
  | grep -v "^d" \
  | awk '{print $8}' \
  | xargs hdfs dfs -cat \
  | python3 scripts/mapper_load_factor.py \
  | python3 scripts/reducer_load_factor.py

hdfs dfs -ls -R /data-lake/raw/velo_stations/ \
  | grep -v "^d" \
  | awk '{print $8}' \
  | xargs hdfs dfs -cat \
  | python3 scripts/mapper_anomalies.py \
  | python3 scripts/reducer_anomalies.py


Supprimer les fichiers corrompus temporaires :
hdfs dfs -rm -r -skipTrash /tmp/hadoop-yarn/staging
hdfs dfs -rm -r -skipTrash /tmp/hadoop-yarn/staging/history

Vérifier que les blocs manquants ont disparu :
hdfs fsck / -list-corruptfileblocks


Supprimer les dossiers load_factor et anomalies s'ils existent avant d'exécuter les commandes hadoop ci-dessous :
hdfs dfs -rm -r -skipTrash /data-lake/processed/load_factor/
hdfs dfs -rm -r -skipTrash /data-lake/processed/anomalies/


Exécuter un traitement distribué Hadoop qui utilise deux scripts Python pour transformer des données brutes et produire un dataset "load_factor" traité :
hadoop jar /opt/hadoop/share/hadoop/tools/lib/hadoop-streaming-3.4.3.jar \
  -D mapreduce.input.fileinputformat.input.dir.recursive=true \
  -file scripts/mapper_load_factor.py \
  -file scripts/reducer_load_factor.py \
  -input /data-lake/raw/velo_stations/ \
  -output /data-lake/processed/load_factor/ \
  -mapper mapper_load_factor.py \
  -reducer reducer_load_factor.py


hadoop jar /opt/hadoop/share/hadoop/tools/lib/hadoop-streaming-3.4.3.jar \
  -D mapreduce.input.fileinputformat.input.dir.recursive=true \
  -file scripts/mapper_anomalies.py \
  -file scripts/reducer_anomalies.py \
  -input /data-lake/raw/velo_stations/ \
  -output /data-lake/processed/anomalies/ \
  -mapper mapper_anomalies.py \
  -reducer reducer_anomalies.py


hdfs dfs -cat /data-lake/processed/load_factor/*
hdfs dfs -cat /data-lake/processed/anomalies/*


Créer les dossiers dans namenode pour la communication avec hive :
hdfs dfs -mkdir -p /data-lake/raw
hdfs dfs -mkdir -p /data-lake/processed
hdfs dfs -mkdir -p /data-lake/curated

hdfs dfs -chmod 777 /data-lake

Désactiver le safemode :
hdfs dfsadmin -safemode leave

Changer le propriétaire et le groupe d'un fichier ou répertoire :
hdfs dfs -chown -R hive:hadoop /data-lake


hdfs dfs -mkdir -p /tmp
hdfs dfs -chmod 777 /tmp
hdfs dfs -chown -R hive:hadoop /tmp

hdfs dfs -mkdir -p /user/hive/warehouse
hdfs dfs -chmod 777 /user/hive/warehouse
hdfs dfs -chown -R hive:hadoop /user

hdfs dfs -mkdir -p /opt/hive/scratch_dir
hdfs dfs -chmod 777 /opt/hive/scratch_dir
hdfs dfs -chown -R hive:hadoop /opt
```

## Commandes dans conteneur hive :
```
Tester si PostgreSQL est joignable :
nc -zv metastore-db 5432

Initialiser le schéma PostgreSQL :
/opt/hive/bin/schematool -dbType postgres -initSchema

Vérifier la version du schéma :
/opt/hive/bin/schematool -dbType postgres -info

Démarrer le service metastore :
hive --service metastore

Vérifier si le metastore est fonctionnel depuis hive-metastore :
netstat -tulpn | grep 9083
ps -ef | grep -i metastore

Vérifier si le metastore est fonctionnel depuis HiveServer2 :
nc -zv hive-metastore 9083

Vérifier quel processus écoute sur le port indiqué :
netstat -tulpn | grep 10000

Vérifier si Hadoop/HDFS fonctionnent :
jps

Ouvrir un client SQL vers Apache Hive depuis HiveServer2 :
beeline -u jdbc:hive2://localhost:10000

Ouvrir un client SQL depuis un autre conteneur :
beeline -u jdbc:hive2://hive-server:10000
```