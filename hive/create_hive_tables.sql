--
-- Base de données :  `velo_stations`
--

-- --------------------------------------------------------

SET hive.execution.engine=tez;

--
-- Structure de la table `raw_velo_stations`
--

CREATE EXTERNAL TABLE raw_velo_stations (
    json STRING
)
STORED AS TEXTFILE
LOCATION '/data-lake/raw/velo_stations/';



--
-- Structure de la table `processed_load_factor`
--

CREATE EXTERNAL TABLE processed_load_factor (
    station_id INT,
    hour BIGINT,
    avg_load_factor DOUBLE,
    std_load_factor DOUBLE,
    validity_ratio STRING
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY '\t'
LOCATION '/data-lake/processed/load_factor/';



--
-- Structure de la table `curated_load_factor`
--

CREATE EXTERNAL TABLE curated_load_factor (
    nb_stations_total INT,
    nb_stations_vides INT,
    proportion_stations_valides DOUBLE
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY '\t'
LOCATION '/data-lake/curated/load_factor/';




--
-- Alimentation de la table `curated_load_factor`
--

INSERT OVERWRITE TABLE curated_load_factor
SELECT
    COUNT(*) AS nb_stations_total,

    SUM(CASE WHEN avg_load_factor = 0 THEN 1 ELSE 0 END)
        AS nb_stations_vides,

    AVG(CASE WHEN validity_ratio LIKE '%/%' THEN
        CAST(SPLIT(validity_ratio, '/')[0] AS DOUBLE) /
        CAST(SPLIT(validity_ratio, '/')[1] AS DOUBLE)
        ELSE 0
    END) AS proportion_stations_valides

FROM processed_load_factor;