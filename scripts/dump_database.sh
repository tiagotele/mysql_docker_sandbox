#!/bin/bash
mysqldump -u root -p --all-databases --ignore-table=mysql.innodb_index_stats --ignore-table=mysql.innodb_table_stats > /scripts/backup.sql 
