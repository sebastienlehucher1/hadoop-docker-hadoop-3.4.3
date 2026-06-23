# Brief Data Lake Vélo Nantes

Pipeline temps réel avec Hadoop / MapReduce / Kafka / Hive


## Mission à satisfaire :


Il s'agit de construire un data lake from scratch qui transforme des données brutes en datasets prêts pour le décisionnel.



## Technologies du projet :


- Conteneurisation Docker

- Apache Hadoop HDFS

- Apache Hadoop MapReduce

- Hive

- Kafka



## Lancement du projet :


La première étape consiste à cloner le dépôt Git depuis l'URL en ligne vers votre machine locale. Cela crée une copie complète du projet, y compris tout l'historique des commits.
Ouvrez votre terminal de VS Code ou votre invite de commandes et utilisez la commande "git clone https://github.com/sebastienlehucher1/hadoop-docker-hadoop-3.4.3.git". Cette commande va créer un dossier avec le nom du dépôt "hadoop-docker-hadoop-3.4.3" et télécharger tous les fichiers du projet à l'intérieur.

Après avoir cloné le dépôt, vous devez vous déplacer dans le dossier qui vient d'être créé pour pouvoir travailler sur le projet en utilisant la commande "cd hadoop-docker-hadoop-3.4.3" dans votre terminal de VS Code.

La liste des commandes docker, hdfs et hive utilisées dans ce projet se trouve dans le fichier "commandes_docker_hdfs_hive.md".

### Construction des conteneurs Docker :
```
docker-compose build
docker-compose up -d
```

### Accès à Hadoop HDFS depuis un navigateur web :

Lorsque dans Docker les conteneurs HDFS datanode, namenode, nodemanager et ressourcemanager fonctionnent, vous pouvez avoir accès à une vue d'ensemble de l'environnement Hadoop HDFS depuis votre navigateur web à l'adresse suivante : http://localhost:9870/dfshealth.html#tab-overview.
Sur la page web principale, vous pouvez consulter les répertoires de fichiers que vous avez créés dans HDFS : onglet Utilities → Browse the file system.


### Accès à Hadoop HDFS depuis le conteneur hive-server :

Quand HiveServer2 accède à HDFS, il utilise le client HDFS pour communiquer avec le Namenode via le port 8020 : il s'agit d'une communication RPC (Remote Procedure Call) Hadoop.

Dans le conteneur hive-server, il est possible de consulter les différents répertoires de fichiers sur HDFS avec les commandes "hdfs dfs -*".
Dans ce conteneur, vous pouvez également ouvrir un client SQL (Beeline) vers Apache Hive. Un client SQL peut exécuter les commandes DDL Hive, y compris la création de tables externes.
'/user/hive/warehouse' est le répertoire par défaut où Hive crée les tables internes/gérées si LOCATION n'est pas spécifié.

