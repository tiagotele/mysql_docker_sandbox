import mysql.connector
# from queries import query_rows_in_tables, query_table_indexes,  query_partitions
from connections import conn_source, conn_target
from compare import same_dicts
from typing import List, Dict

def fetch_rows_per_table(cursor, query) -> List[Dict[str, int]]:
    cursor.execute(query)
    results = cursor.fetchall()
    return [{row[0]: row[1]} for row in results]

def compare_datasets_based_in_query(cursor_source, cursor_target, query):
    rows_per_table_source = fetch_rows_per_table(cursor_source, query)
    rows_per_table_target = fetch_rows_per_table(cursor_target, query)
    if same_dicts(rows_per_table_source, rows_per_table_target, True):
        print("Same nubmer of rows in each database")
    else:
        print("Different nubmer of rows in each database")

def main():
    try:
        with conn_source.cursor() as cursor_source, conn_target.cursor() as cursor_target:
            # compare_datasets_based_in_query(cursor_source, cursor_target, query_rows_in_tables)
            compare_datasets_based_in_query(cursor_source, cursor_target, query_table_indexes)
            compare_datasets_based_in_query(cursor_source, cursor_target, query_partitions)
    except mysql.connector.Error as err:
        print(f"Error {err}")
    finally:
        conn_source.close()
        conn_target.close()

if __name__ == "__main__":
    main()