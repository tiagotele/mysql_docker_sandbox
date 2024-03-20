#!/bin/bash
mysqldump -u root --all-databases -p > /scripts/backup.sql 
