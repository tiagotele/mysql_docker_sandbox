import mysql.connector
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import random
from faker import Faker
from connector_settings import config1, config2

MAX_WORKERS=32

# List of tables for which you want to run SELECT COUNT(*)
tables = [
    "SELECT COUNT(1) FROM test.people;",
    "SELECT COUNT(1) FROM test.companies;",
    "SELECT COUNT(1) FROM test.cars;",
    "SELECT COUNT(1) FROM test.products;",
    "SELECT COUNT(1) FROM test.orders;",
    "SELECT COUNT(1) FROM test.employees;",
    "SELECT COUNT(1) FROM test.departments;",
    "SELECT COUNT(1) FROM test.cities;",
    "SELECT COUNT(1) FROM test.countries;",
    "SELECT COUNT(1) FROM test.books;",
    ]

tables2 = [
    "SELECT COUNT(1) FROM test2.people;",
    "SELECT COUNT(1) FROM test2.companies;",
    "SELECT COUNT(1) FROM test2.cars;",
    "SELECT COUNT(1) FROM test2.products;",
    "SELECT COUNT(1) FROM test2.orders;",
    "SELECT COUNT(1) FROM test2.employees;",
    "SELECT COUNT(1) FROM test2.departments;",
    "SELECT COUNT(1) FROM test2.cities;",
    "SELECT COUNT(1) FROM test2.countries;",
    "SELECT COUNT(1) FROM test2.books;",
    ]

# Function to execute the SELECT COUNT(*) query
def run_query(conn_config, query):

    cnx = None
    cursor = None
    try:
        start = time.time()
        cnx = mysql.connector.connect(**conn_config)
        cursor = cnx.cursor()

        cursor.execute(query)
        result = cursor.fetchone()

        end = time.time()
        total = end - start
        print(
            f"\nQuery = {query}.\nTotal = {result[0]}. Query execution time: {total:.3f}"
        )

        return query, result[0]

    except mysql.connector.Error as err:
        return query, f"Error: {err}"

    finally:
        if cursor:
            cursor.close()
        if cnx:
            cnx.close()


# Execute queries in parallel using ThreadPoolExecutor
def execute_queries_in_parallel(tables):
    print("Starting queries")
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        future_to_table1 = {executor.submit(run_query, config1, table): table for table in tables}
        future_to_table2 = {executor.submit(run_query, config2, table): table for table in tables2}

        for future in as_completed(future_to_table1):
            table = future_to_table1[future]
            try:
                data = future.result(timeout=10)
                print(f"DONE = {data}")
            except Exception as exc:
                print(f"Query: {table} generated an exception: {exc}")

        for future in as_completed(future_to_table2):
            table = future_to_table2[future]
            try:
                data = future.result(timeout=10)
                print(f"DONE = {data}")
            except Exception as exc:
                print(f"Query: {table} generated an exception: {exc}")

    print("pool finished")
    

if __name__ == "__main__":
    s = time.time()
    execute_queries_in_parallel(tables)
    e = time.time()
    total_time = e - s
    print(f"Total time = {total_time:.3f}")
    print("END")
