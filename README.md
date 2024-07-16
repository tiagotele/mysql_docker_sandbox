# MySQL Docker

Creating sample database in MySQL version 5.7. Check for compatibility for upgrade version, exporting dump database and reloading into MySQL version 8.0

___

# Exporting data from MySQL version 5.7
```bash
./init_mysql8.sh
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
./init_mysql8.sh
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

---

# Check for differences between MySQL 5.7 and 8.3

Firstly run the both databases with Docker compose:
```bash
docker compose up
```

Then run the Python script:
```bash
python3 compare_db.py
```
