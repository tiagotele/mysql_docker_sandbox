import mysql.connector

conn_source = mysql.connector.connect(
    host="localhost",
    port = 3306,
    user="root",
    password="1234",
    database="information_schema"
)

conn_target = mysql.connector.connect(
    host="localhost",
    port = 3307,
    user="root",
    password="1234",
    database="information_schema"
)

query_rows_in_tables = """
SELECT
	table_name AS 'table',
    table_rows AS 'rows'
FROM
	tables
WHERE
	table_schema in ('test')
ORDER BY
	table_rows DESC
;
"""

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
