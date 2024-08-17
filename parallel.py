import mysql.connector
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import random

# MySQL connection configuration
config = {
    'user': 'root',
    'password': '1234',
    'host': 'localhost',
    'port': 3306,
    'database': 'test',
    'pool_name': 'mypool',
    'pool_size': 10  # Ensure this matches the number of threads or more
}
# config = {
#     "user": "caylent_user",
#     "password": "[Rent@lbe@stC@ylent]",
#     "host": "qa-instance-aurora-caylent-clone-dms-0-cluster.cluster-cy4xvmuy53uf.us-east-1.rds.amazonaws.com",
#     "port": 3306,
#     "database": "rb_dev",
#     "pool_name": "mypool",
#     "pool_size": 32,  # Ensure this matches the number of threads or more
# }

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
    with ThreadPoolExecutor(max_workers=32) as executor:
        future_to_table = {executor.submit(run_query, config, table): table for table in tables}

        for future in as_completed(future_to_table):
            table = future_to_table[future]
            try:
                data = future.result(timeout=10)
                # print(f"Query: {data[0]}, Count: {data[1]}")
                print(f"DONE = {data}")
            except Exception as exc:
                print(f"Query: {table} generated an exception: {exc}")


if __name__ == "__main__":
    s = time.time()
    execute_queries_in_parallel(tables)
    e = time.time()
    total_time = e - s
    print(f"Total time = {total_time:.3f}")
    print("END")
