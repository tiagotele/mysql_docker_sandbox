#!/bin/bash
docker run \
    --name='my_sql_container_new' \
    -p 33011:3306 \
    -e MYSQL_ROOT_PASSWORD=1234 \
    -v ./init_db8:/docker-entrypoint-initdb.d \
    -v ./scripts:/scripts \
    mysql:8.3.0
