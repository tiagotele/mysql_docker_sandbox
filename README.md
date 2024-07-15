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
# Importing data into MySQL version 8.3.0

## Running MySQL 8.3.0
```bash
    docker run \
    --name='my_sql_container_new' \
    -p 3307:3306 \
    -e MYSQL_ROOT_PASSWORD=1234 \
    -v ./scripts:/scripts \
    mysql:8.3.0
```

## Operations inside MySQL in Docker
Enter MySQL container with this command:
```bash
docker exec -it my_sql_container_new bash 
```

### Loading dump into current MySQL instance

```bash
mysql -u root -p < scripts/backup.sql 
```

Now you can see the databases and tables in new MySQL 8.3.0