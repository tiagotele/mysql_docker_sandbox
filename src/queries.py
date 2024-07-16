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


query_table_indexes = """
SELECT  
	table_schema,
	table_name,
	index_name,
	column_name
FROM 
	information_schema.statistics
WHERE 
	non_unique = 1
AND 
	table_schema in ('test')
;
"""

query_partitions = """
SELECT 
    *
FROM 
    information_schema.partitions
WHERE 
    TABLE_SCHEMA in ('test')
    AND PARTITION_NAME IS NOT NULL
;
"""