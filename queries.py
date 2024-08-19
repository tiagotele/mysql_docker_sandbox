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
QUERY_1_VERSIONS = """
SELECT VERSION();
"""
QUERY_2_VARIABLES = """
SHOW VARIABLES;
"""

QUERY_3_SCHEMAS_LIST = """
SHOW DATABASES;
"""

QUERY_4_LIST_TABLES = """
SELECT
	table_name AS 'table'
FROM
	information_schema.tables
WHERE
    table_schema like 'rb%'
ORDER BY
	table_schema
;
"""

QUERY_5_LIST_VIEWS = """
SELECT
	table_name AS 'table'
FROM
	INFORMATION_SCHEMA.VIEWS
WHERE
    table_schema like 'rb%'
ORDER BY
	table_name
;
"""

QUERY_6_LIST_CONSTRAINTS = """
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
	TABLE_SCHEMA like 'rb%'
;
"""

QUERY_7_LIST_INDEXES = """
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
    table_schema like "rb%"
;
"""

QUERY_8_LIST_PARTITIONS = """
SELECT 
    *
FROM 
    information_schema.partitions
WHERE 
    TABLE_SCHEMA like 'rb%'
    AND PARTITION_NAME IS NOT NULL
;
"""

QUERY_9_LIST_STORED_PROCEDURES = """
SELECT  
    routine_schema,  
    routine_name,  
    routine_type 
FROM 
    information_schema.routines 
WHERE 
    routine_schema like 'rb%'
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
	TRIGGER_SCHEMA not in ("mysql") # native mysql not required for compare in migrations
;
"""

QUERY_11_LIST_USERS_AND_HOSTS = """
SELECT User, Host FROM mysql.user;
"""

QUERY_12_LIST_USERS_AND_ITS_PERMISSIONS = """
SELECT User FROM mysql.user;
"""