# MySQL Docker

## MySQL version 5.7 in Docker
```bash
docker run --name='my_sql_container'  -p 3306:3306 -e MYSQL_ROOT_PASSWORD=1234 -v ./init_db:/docker-entrypoint-initdb.d mysql/mysql-server:5.7 
```