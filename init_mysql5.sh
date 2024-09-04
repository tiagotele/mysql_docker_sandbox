#!/bin/bash
docker run \
    --name='my_sql_container' \
    -p 33010:3306 \
    -e MYSQL_ROOT_PASSWORD=1234 \
    -v ./init_db:/docker-entrypoint-initdb.d \
    -v ./scripts:/scripts \
    mysql/mysql-server:5.7
