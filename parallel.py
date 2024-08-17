import mysql.connector
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import random
from faker import Faker


MAX_WORKERS=32

# MySQL connection configuration
config = {
    'user': 'root',
    'password': '1234',
    'host': 'localhost',
    'port': 3310,
    'database': 'test',
    'pool_name': 'mypool',
    'pool_size': 20  # Ensure this matches the number of threads or more
}
config2 = {
    'user': 'root',
    'password': '1234',
    'host': 'localhost',
    'port': 33011,
    'database': 'test',
    'pool_name': 'mypool2',
    'pool_size': 20  # Ensure this matches the number of threads or more
}

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

fake = Faker()

def insert_data(conn_config, num_rows):
    
    cnx = mysql.connector.connect(**conn_config)
    cursor = cnx.cursor()

    # Table 1: People
    for _ in range(num_rows):
        sql = "INSERT INTO people (first_name, last_name, birth_date, email, phone_number) VALUES (%s, %s, %s, %s, %s)"
        val = (fake.first_name(), fake.last_name(), fake.date_of_birth(minimum_age=18, maximum_age=90), fake.email(), fake.phone_number())
        cursor.execute(sql, val)
    
    # Table 2: Companies
    for _ in range(num_rows):
        sql = "INSERT INTO companies (company_name, founded_date, industry, ceo_name) VALUES (%s, %s, %s, %s)"
        val = (fake.company(), fake.date_between(start_date='-100y', end_date='today'), fake.bs(), fake.name())
        cursor.execute(sql, val)
    
    # Table 3: Cars
    for _ in range(num_rows):
        sql = "INSERT INTO cars (make, model, year, price, color) VALUES (%s, %s, %s, %s, %s)"
        val = (fake.company(), fake.word(), random.randint(1990, 2024), round(random.uniform(5000, 50000), 2), fake.color_name())
        cursor.execute(sql, val)
    
    # Table 4: Products
    for _ in range(num_rows):
        sql = "INSERT INTO products (product_name, category, price, stock_quantity) VALUES (%s, %s, %s, %s)"
        val = (fake.word(), fake.word(), round(random.uniform(10, 1000), 2), random.randint(0, 1000))
        cursor.execute(sql, val)
    
    # Table 5: Orders
    for _ in range(num_rows):
        sql = "INSERT INTO orders (order_date, customer_name, total_amount, status) VALUES (%s, %s, %s, %s)"
        val = (fake.date_this_decade(), fake.name(), round(random.uniform(100, 5000), 2), random.choice(['Pending', 'Shipped', 'Delivered', 'Cancelled']))
        cursor.execute(sql, val)
    
    # Table 6: Employees
    for _ in range(num_rows):
        sql = "INSERT INTO employees (first_name, last_name, hire_date, position, salary) VALUES (%s, %s, %s, %s, %s)"
        val = (fake.first_name(), fake.last_name(), fake.date_between(start_date='-30y', end_date='today'), fake.job(), round(random.uniform(30000, 200000), 2))
        cursor.execute(sql, val)
    
    # Table 7: Departments
    for _ in range(num_rows):
        sql = "INSERT INTO departments (department_name, manager_name, budget) VALUES (%s, %s, %s)"
        val = (fake.word(), fake.name(), round(random.uniform(50000, 1000000), 2))
        cursor.execute(sql, val)
    
    # Table 8: Cities
    for _ in range(num_rows):
        sql = "INSERT INTO cities (city_name, country, population, area_km2) VALUES (%s, %s, %s, %s)"
        val = (fake.city(), fake.country(), random.randint(10000, 10000000), round(random.uniform(10.0, 1000.0), 2))
        cursor.execute(sql, val)
    
    # Table 9: Countries
    continents = ['Africa', 'Asia', 'Europe', 'North America', 'South America', 'Oceania', 'Antarctica']
    for _ in range(num_rows):
        sql = "INSERT INTO countries (country_name, continent, population, gdp_trillions) VALUES (%s, %s, %s, %s)"
        val = (fake.country(), random.choice(continents), random.randint(1000000, 1400000000), round(random.uniform(0.1, 25.0), 2))
        cursor.execute(sql, val)
    
    # Table 10: Books
    for _ in range(num_rows):
        sql = "INSERT INTO books (title, author, publish_date, genre, price) VALUES (%s, %s, %s, %s, %s)"
        val = (fake.catch_phrase(), fake.name(), fake.date_between(start_date='-100y', end_date='today'), random.choice(['Fiction', 'Non-fiction', 'Science Fiction', 'Biography', 'History', 'Fantasy']), round(random.uniform(5, 100), 2))
        cursor.execute(sql, val)

    cnx.commit()  # Commit the transaction

    cursor.close()
    cnx.close()


# Close the connection

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
        future_to_table2 = {executor.submit(run_query, config, table): table for table in tables}
        future_to_table2 = {executor.submit(run_query, config2, table): table for table in tables2}

        for future in as_completed(future_to_table2):
            table = future_to_table2[future]
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
    # Call the function with the desired number of rows
    # insert_data(config, 10)
    # insert_data(config2, 10)
