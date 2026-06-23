#!/bin/bash
set -e

echo "Starting Hive Metastore..."

# Lancer le metastore
exec hive --service metastore