import mysql.connector
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import random

# MySQL connection configuration
config = {
    'user': 'root',
    'password': '1234',
    'host': 'localhost',
    'port': 3307,
    'database': 'test',
    'pool_name': 'mypool',
    'pool_size': 10  # Ensure this matches the number of threads or more
}

# List of tables for which you want to run SELECT COUNT(*)
tables = ["people", "companies", "cars", "products", "orders", "employees", "departments", "cities", "countries", "books"]



# Function to execute the SELECT COUNT(*) query
def run_query(table):
    cnx = None
    cursor = None
    random_int = random.randint(1,3)
    print(f"Running table {table} taking {random_int} seconds \n")
    time.sleep(random_int)
    try:
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()

        query = f"SELECT COUNT(*) FROM {table}"
        cursor.execute(query)
        result = cursor.fetchone()

        return table, result[0]

    except mysql.connector.Error as err:
        return table, f"Error: {err}"

    finally:
        if cursor:
            cursor.close()
        if cnx:
            cnx.close()

# Execute queries in parallel using ThreadPoolExecutor
def execute_queries_in_parallel(tables):
    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_table = {executor.submit(run_query, table): table for table in tables}

        for future in as_completed(future_to_table):
            table = future_to_table[future]
            try:
                data = future.result()
                print(f"Table: {data[0]}, Count: {data[1]}")
            except Exception as exc:
                print(f"Table: {table} generated an exception: {exc}")

if __name__ == "__main__":
    s=time.time()
    execute_queries_in_parallel(tables)
    e=time.time()
    total_time=e-s
    print(f"Total time = {total_time:.3f}")