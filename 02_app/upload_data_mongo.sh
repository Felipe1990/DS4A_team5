PATH_CURRENT = $pwd 
mongoimport \
--host Cluster0-shard-0/cluster0-shard-00-00-2stua.mongodb.net:27017,cluster0-shard-00-01-2stua.mongodb.net:27017,cluster0-shard-00-02-2stua.mongodb.net:27017 \
--ssl --username felipe_A --password sUIluNvmD1d0RbCB \
--authenticationDatabase admin --db DS4A --collection census_information --type csv \
--file "/home/felipe/Documents/DS4A/Creditas/Copy of censitarios/repo/02_app/data_censo_sp.csv" --headerline