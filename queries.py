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
