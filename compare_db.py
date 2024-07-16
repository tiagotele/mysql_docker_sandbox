import mysql.connector
from queries import query_rows_in_tables
from connections import conn_source, conn_target

cursor_source = conn_source.cursor()
cursor_source.execute(query_rows_in_tables)

cursor_target = conn_target.cursor()
cursor_target.execute(query_rows_in_tables)

results_source = cursor_source.fetchall()
results_target = cursor_target.fetchall()

rows_per_table_source = []
for row in results_source:
    rows_per_table_source.append({row[0]: row[1]})

print(rows_per_table_source)

rows_per_table_target = []
for row in results_target:
    rows_per_table_target.append({row[0]: row[1]})

print(rows_per_table_target)

cursor_source.close()
conn_source.close()
