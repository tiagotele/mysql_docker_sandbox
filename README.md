# MySQL Docker

Creating sample database in MySQL version 5.7. Check for compatibility for upgrade version, exporting dump database and reloading into MySQL version 8.0

___

# Exporting data from MySQL version 5.7
```bash
    docker run \
    --name='my_sql_container' \
    -p 3306:3306 \
    -e MYSQL_ROOT_PASSWORD=1234 \
    -v ./init_db:/docker-entrypoint-initdb.d \
    -v ./scripts:/scripts \
    mysql/mysql-server:5.7 
```

## Operations inside MySQL in Docker

Enter MySQL container with this command:
```bash
docker exec -it my_sql_container bash 
```

### Pre-flight check
```bash
./scripts/pre_flight_update_check.sh
```

### Dump file
```bash
./scripts/dump_databaes.sh
```
___
# Importing data into MySQL version 8.0
TBD