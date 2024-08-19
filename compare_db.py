import os
import time
import mysql.connector


################################################
# ENV VARS
################################################
LIMIT_COUNT_TABLES=os.getenv("LIMIT_COUNT_TABLES", "")
LIMIT_COUNT_VIEWS=os.getenv("LIMIT_COUNT_VIEWS", "")

ENV_NAME_SRC = os.getenv("ENV_NAME_SRC")
HOST_SRC = os.getenv("HOST_SRC")
USER_SRC = os.getenv("USER_SRC")
PASSWORD_SRC = os.getenv("PASSWORD_SRC")
DATABASE_SRC = os.getenv("DATABASE_SRC")
PORT_SRC = os.getenv("PORT_SRC")

ENV_NAME_DEST = os.getenv("ENV_NAME_DEST")
HOST_DEST = os.getenv("HOST_DEST")
USER_DEST = os.getenv("USER_DEST")
PASSWORD_DEST = os.getenv("PASSWORD_DEST")
DATABASE_DEST = os.getenv("DATABASE_DEST")
PORT_DEST = os.getenv("PORT_DEST")

SCHEMA_TO_USE=DATABASE_SRC

if not all([ENV_NAME_SRC, HOST_SRC, USER_SRC, PASSWORD_SRC, DATABASE_SRC, PORT_SRC]):
    raise EnvironmentError("Missing environment variables for source database")
if not all([ENV_NAME_DEST, HOST_DEST, USER_DEST, PASSWORD_DEST, DATABASE_DEST, PORT_DEST]):
    raise EnvironmentError("Missing environment variables for destination database")


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


TOP_TABLES = f"""
SELECT
    table_schema, 
	table_name AS 'table'
FROM
    information_schema.tables
WHERE
    table_schema = '{SCHEMA_TO_USE}'
    and TABLE_TYPE = 'BASE TABLE'
    and TABLE_NAME <> 'listings_aj_properties'
ORDER BY
    table_rows ASC, table_name ASC
{LIMIT_COUNT_TABLES}
"""

TOP_VIEWS = f"""
SELECT
    table_schema, 
	table_name AS 'table'
FROM
    information_schema.tables
WHERE
    table_schema = '{SCHEMA_TO_USE}'
    and TABLE_TYPE = 'VIEW'
ORDER BY
    table_rows ASC, table_name ASC
{LIMIT_COUNT_VIEWS}
"""

FETCH_FIRST_N_ROWS_FROM_TABLE="""
SELECT
    *
FROM 
    {table}
ORDER BY 1
LIMIT {limit}
;
"""

conn_src = mysql.connector.connect(
    host=HOST_SRC,
    port=PORT_SRC,
    user=USER_SRC,
    password=PASSWORD_SRC,
    database=DATABASE_SRC
)

conn_dest = mysql.connector.connect(
    host=HOST_DEST,
    port=PORT_DEST,
    user=USER_DEST,
    password=PASSWORD_DEST,
    database=DATABASE_DEST
)

tables_to_validate_content = [
    f"{SCHEMA_TO_USE}.users",
    f"{SCHEMA_TO_USE}.listings_aj",
    f"{SCHEMA_TO_USE}.partner_company",
    f"{SCHEMA_TO_USE}.regions",
    f"{SCHEMA_TO_USE}.featured_areas"
]


def fetch_list_from_set(current_set):
    return list(map(lambda x: x[0], current_set))

def fetch_dict_from_set(current_set):
    a = list(map(lambda x: {x[0]: x[1]}, current_set))
    return sorted(a, key=lambda d: next(iter(d)))

def show_diff(l1: list = [], l2: list = [], transformation = fetch_list_from_set):
    diff_source_target = set(l1) - set(l2)
    diff_target_source = set(l2) - set(l1)

    if diff_source_target != set():
        print(f"\n\n{ENV_NAME_DEST} doesn't have this elements:")
        it = transformation(diff_source_target)
        for i in it:
            print(i)

    if diff_target_source != set():
        print(f"\n\n{ENV_NAME_SRC} doesn't have this elements:")
        it = transformation(diff_target_source)
        for i in it:
            print(i)



def tuples_list_are_equal(l1: list = [], l2: list = []) -> bool:
    equal_result = False

    if len(l1) != len(l2):
        return equal_result

    if set(l1) - set(l2) == set() and set(l2) - set(l1) == set():
        equal_result = True
    return equal_result


def compare(purpose, query, cursor_src, cursor_dest, transformation = fetch_list_from_set):
    print("\n\n------------------------------------------------")
    print(f"Comparing {purpose}")
    
    try:
        cursor_src.execute(query)
        result_src = cursor_src.fetchall()

        cursor_dest.execute(query)
        result_dest = cursor_dest.fetchall()
    except mysql.connector.Error as err:
        print(f"Error: {err}")

    if tuples_list_are_equal(result_src, result_dest):
        print("equal")
    else:
        print("different")
        show_diff(result_src, result_dest, transformation)

    if len(result_src) != len(result_dest):
        print(f"Total itens in {ENV_NAME_SRC} = {len(result_src)}")
        print(f"Total itens in {ENV_NAME_DEST} = {len(result_dest)}")

def show_user_grant(environment: str ,users_and_hosts:tuple, cursor):
    print("\n\n-----------------------")
    print(f"Users and permissions in {environment}")
    for result in users_and_hosts:
        query = f"SHOW GRANTS FOR '{result[0]}'@'{result[1]}';"
        print(f"----user {result[0]}")
        try:
            cursor.execute(query)
            query_result = cursor.fetchall()
            for row in query_result:
                for item in row:
                    print(item)
        except mysql.connector.Error as err:
            print(f"Error = {err}")
    

def users_and_permissions(purpose, query, cursor_src, cursor_dest):
    print("\n\n------------------------------------------------")
    print(f"Comparing {purpose}\n")
    
    # fetch users and hosts
    try:
        cursor_src.execute(QUERY_11_LIST_USERS_AND_HOSTS)
        result_src = cursor_src.fetchall()
        
        cursor_dest.execute(QUERY_11_LIST_USERS_AND_HOSTS)
        result_dest = cursor_dest.fetchall()
    except mysql.connector.Error as err:
        print(f"Error = {err}")
    
    # print("\n\n-----------------------")
    # print(f"Users and permissions in {ENV_NAME_SRC}")
    show_user_grant(ENV_NAME_SRC, result_src, cursor_src)
    show_user_grant(ENV_NAME_DEST, result_dest, cursor_dest)
    

def first_phase_compare(cursor_src, cursor_dest):
        compare("1 Version", QUERY_1_VERSIONS, cursor_src, cursor_dest)
        compare("2 Variables", QUERY_2_VARIABLES, cursor_src, cursor_dest, fetch_dict_from_set)
        compare("3 Schemas", QUERY_3_SCHEMAS_LIST, cursor_src, cursor_dest)
        compare("4 Tables", QUERY_4_LIST_TABLES, cursor_src, cursor_dest)
        compare("5 Views", QUERY_5_LIST_VIEWS, cursor_src, cursor_dest)
        compare("6 Constraints", QUERY_6_LIST_CONSTRAINTS, cursor_src, cursor_dest)
        compare("7 Indexes", QUERY_7_LIST_INDEXES, cursor_src, cursor_dest)
        compare("8 Paritions", QUERY_8_LIST_PARTITIONS, cursor_src, cursor_dest)
        compare( "9 Stored procedures", QUERY_9_LIST_STORED_PROCEDURES, cursor_src, cursor_dest,)
        compare("10 Trigges", QUERY_10_LIST_TRIGGERS, cursor_src, cursor_dest)
        compare( "11 Users", QUERY_11_LIST_USERS_AND_HOSTS, cursor_src, cursor_dest,)
        users_and_permissions( "12 Users and Permissions", QUERY_12_LIST_USERS_AND_ITS_PERMISSIONS, cursor_src, cursor_dest,)

def compare_dicts(dict_a, dict_b):
    all_keys = set(dict_a.keys()).union(set(dict_b.keys()))

    print(f"table,blue,green,comparator")
    for key in all_keys:
        value_a = dict_a.get(key, "N/A")
        value_b = dict_b.get(key, "N/A")

        if value_a == "N/A" or value_b == "N/A":
            status = "different"
        elif value_a == value_b:
            status = "equal"
        else:
            status = "different"

        print(f"{key},{value_a},{value_b},{status}")


def count_rows(query, cursor):
    table_count = {}
    try:
        cursor.execute(query)
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    top_views = cursor.fetchall()

    for views in top_views:
        start_time = time.time()
        entity = f"{views[0]}.{views[1]}"
        query = f"SELECT COUNT(1) FROM {entity};"
        print(query)
        try:
            cursor.execute(query)
            total = cursor.fetchall()
            print((total[0][0]))
            table_count[entity] = (total[0][0])
        except mysql.connector.Error as err:
            print(f"Error: {err}")
    
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Query execution time: {execution_time:.3f} seconds\n")
    return table_count

def second_phase_compare(cursor_src, cursor_dest):
        print("--------------------------")
        print(f"Counting total tables in {ENV_NAME_SRC}")
        start=time.time()
        count_tables_src = count_rows(TOP_TABLES,cursor_src)
        end=time.time()
        total=start-end
        print(f"\nTotal time for count tables in {ENV_NAME_SRC} is {total:.3f} seconds.\n")

        print(f"Counting total views in {ENV_NAME_SRC}")
        start=time.time()
        count_rows(TOP_VIEWS,cursor_src)
        end=time.time()
        total=start-end
        print(f"\nTotal time for count views in {ENV_NAME_SRC} is {total:.3f} seconds.\n")
        
        print("--------------------------")
        print(f"Counting total tables in {ENV_NAME_DEST}")
        start=time.time()
        count_tables_dest = count_rows(TOP_TABLES,cursor_dest)
        end=time.time()
        total=start-end
        print(f"\nTotal time for count tables in {ENV_NAME_DEST} is {total:.3f} seconds.\n")

        print(f"Counting total views in {ENV_NAME_DEST}")
        start=time.time()
        count_rows(TOP_VIEWS,cursor_dest)
        end=time.time()
        total=start-end
        print(f"\nTotal time for count views in {ENV_NAME_DEST} is {total:.3f} seconds.\n")
        print(f"Counting total views in {ENV_NAME_DEST}")
        
        compare_dicts(count_tables_src, count_tables_dest)


def column_id_name(table_name, cursor):
    query = f"SHOW COLUMNS FROM {table_name};"
    try:
        cursor.execute(query)
        colum_names = cursor.fetchall()
    except mysql.connector.Error as err:
        print(f"Error = {err}")
    return colum_names[0][0]

def third_phase(cursor_src, cursor_dest):
    for table in tables_to_validate_content:
        print(f"\nComparing rows in table {table}")
        query = FETCH_FIRST_N_ROWS_FROM_TABLE.format(table = table, limit = 10)
        try:
            cursor_src.execute(query)
            source_data = cursor_src.fetchall()
            source_ids = [row[0] for row in source_data]
            placeholders = ','.join(['%s'] * len(source_ids))
        except mysql.connector.Error as err:
            print(f"Error: {err}")

        
        column_name = column_id_name(table, cursor_dest)
        query_dest = f"SELECT * FROM {table} where {column_name} IN ({placeholders})"
        cursor_dest.execute(query_dest, source_ids)
        dest_data = cursor_dest.fetchall()
        
        if sorted(source_data) == sorted(dest_data):
            print("Data is equal")
        else:
            print("Data is different")
            print(f"Ids in table: {source_ids}")

def main():
    start_time = time.time()
    try:
        with conn_src.cursor() as cursor_src, conn_dest.cursor() as cursor_dest:
            first_phase_compare(cursor_src, cursor_dest)
            second_phase_compare(cursor_src, cursor_dest)
            third_phase(cursor_src, cursor_dest)
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
    except Exception as e:
        print(f"Unexpected error: {e}")
    finally:
        conn_src.close()
        print("Connection source closed.")
        conn_dest.close()
        print("Connection destiny closed.")
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Report total time: {execution_time:.3f} seconds\n")


if __name__ == "__main__":
    main()
