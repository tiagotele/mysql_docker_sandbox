import time
import mysql.connector
from pycparser.ply.yacc import resultlimit

################################################
# QUERIES
################################################
# 1 - MYSQL VERSION
# 2 - ENVIONMENT VARIABLES - PARAMETER GROUP
# 3 - SCHEMAS LIST
# 4 - TABLES LIST - RBDEV
# 5 - VIEWS LIST - RBDEV
# 6 - CONSTRAINTS LIST
# 7 - INDEXES LIST
# 8 - PARTITIONS LIST
# 9 - STORED PROCEDURES LIST
# 10 - TRIGGERS LIST
# 11 - USERS
# 12 - USERS AND ITS PERMISSIONS
QUERY_01_VERSIONS = """
SELECT VERSION();
"""
QUERY_02_VARIABLES = """
SHOW VARIABLES;
"""

QUERY_03_SCHEMAS_LIST = """
SHOW DATABASES;
"""

QUERY_04_LIST_TABLES = """
SELECT
	table_name AS 'table'
FROM
	information_schema.tables
WHERE
    table_schema like 'test%'
ORDER BY
	table_schema
;
"""

QUERY_05_LIST_VIEWS = """
SELECT
	table_name AS 'table'
FROM
	INFORMATION_SCHEMA.VIEWS
WHERE
    table_schema like 'test%'
ORDER BY
	table_name
;
"""

QUERY_06_LIST_CONSTRAINTS = """
SELECT 
	# CONSTRAINT_CATALOG,
	# CONSTRAINT_SCHEMA,
	CONSTRAINT_NAME,
	# TABLE_SCHEMA,
	TABLE_NAME,
	CONSTRAINT_TYPE
FROM 
    information_schema.TABLE_CONSTRAINTS AS tc
WHERE 
	TABLE_SCHEMA like 'test`%'
;
"""

QUERY_07_LIST_INDEXES = """
SELECT  
    # table_schema,
    table_name,
    index_name,
    column_name
FROM 
    information_schema.statistics
WHERE 
    non_unique = 1
AND 
    table_schema like "test`%"
;
"""

QUERY_08_LIST_PARTITIONS = """
SELECT 
    *
FROM 
    information_schema.partitions
WHERE 
    TABLE_SCHEMA like 'test`%'
    AND PARTITION_NAME IS NOT NULL
;
"""

QUERY_09_LIST_STORED_PROCEDURES = """
SELECT  
    routine_schema,  
    routine_name,  
    routine_type 
FROM 
    information_schema.routines 
WHERE 
    routine_schema like 'test`%'
ORDER BY 
    routine_name
;
"""

QUERY_10_LIST_TRIGGERS = """
SELECT 
	TRIGGER_NAME, EVENT_MANIPULATION, EVENT_OBJECT_TABLE
FROM 
	information_schema.TRIGGERS
WHERE 
	TRIGGER_SCHEMA not in ("mysql")
;
"""

QUERY_11_LIST_USERS_AND_HOSTS = """
SELECT User, Host FROM mysql.user;
"""

QUERY_12_LIST_USERS_AND_ITS_PERMISSIONS = """
SELECT User FROM mysql.user;
"""

TOP_TABLES = f"""
SELECT
    table_schema, 
	table_name AS 'table'
FROM
    information_schema.tables
WHERE
    TABLE_SCHEMA NOT IN ('mysql', 'performance_schema', 'sys')
    AND TABLE_TYPE = 'BASE TABLE'
ORDER BY
    table_rows ASC, table_name ASC
"""

QUERIES_FIRST_PHASE = {
    "QUERY_01_VERSIONS": QUERY_01_VERSIONS,
    "QUERY_02_VARIABLES": QUERY_02_VARIABLES,
    "QUERY_03_SCHEMAS_LIST": QUERY_03_SCHEMAS_LIST,
    "QUERY_04_LIST_TABLES": QUERY_04_LIST_TABLES,
    "QUERY_05_LIST_VIEWS": QUERY_05_LIST_VIEWS,
    "QUERY_06_LIST_CONSTRAINTS": QUERY_06_LIST_CONSTRAINTS,
    "QUERY_07_LIST_INDEXES": QUERY_07_LIST_INDEXES,
    "QUERY_08_LIST_PARTITIONS": QUERY_08_LIST_PARTITIONS,
    "QUERY_09_LIST_STORED_PROCEDURES": QUERY_09_LIST_STORED_PROCEDURES,
    "QUERY_10_LIST_TRIGGERS": QUERY_10_LIST_TRIGGERS,
    "QUERY_11_LIST_USERS_AND_HOSTS": QUERY_11_LIST_USERS_AND_HOSTS,
    "QUERY_12_LIST_USERS_AND_ITS_PERMISSIONS": QUERY_12_LIST_USERS_AND_ITS_PERMISSIONS,
}



def run_query(conn_config, name, query) -> tuple:

    cnx = None
    cursor = None
    try:
        start = time.time()
        cnx = mysql.connector.connect(**conn_config)
        cursor = cnx.cursor()

        cursor.execute(query)
        result = cursor.fetchall()

        end = time.time()
        total = end - start
        # print(
        #     f"\nQuery = {query}.\nTotal = {result[0]}. Query execution time: {total:.3f}"
        # )

        return name, query, result

    except mysql.connector.Error as err:
        return query, f"The query {query} ran with error: {err}"
    except Exception as ex:
        return name, f"Query execution error: {ex}"

    finally:
        if cursor:
            cursor.close()
        if cnx:
            cnx.close()
