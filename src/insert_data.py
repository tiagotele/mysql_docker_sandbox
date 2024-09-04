import mysql.connector
from faker import Faker
import random
from connector_settings import  connections

fake = Faker()

def insert_data(conn_config, num_rows):
    
    cnx = mysql.connector.connect(**conn_config)
    cursor = cnx.cursor()

    # Table 1: People
    for _ in range(num_rows):
        sql = "INSERT INTO test.people (first_name, last_name, birth_date, email, phone_number) VALUES (%s, %s, %s, %s, %s)"
        val = (fake.first_name(), fake.last_name(), fake.date_of_birth(minimum_age=18, maximum_age=90), fake.email(), fake.phone_number())
        cursor.execute(sql, val)
    
    # Table 2: Companies
    for _ in range(num_rows):
        sql = "INSERT INTO test.companies (company_name, founded_date, industry, ceo_name) VALUES (%s, %s, %s, %s)"
        val = (fake.company(), fake.date_between(start_date='-100y', end_date='today'), fake.bs(), fake.name())
        cursor.execute(sql, val)
    
    # Table 3: Cars
    for _ in range(num_rows):
        sql = "INSERT INTO test.cars (make, model, year, price, color) VALUES (%s, %s, %s, %s, %s)"
        val = (fake.company(), fake.word(), random.randint(1990, 2024), round(random.uniform(5000, 50000), 2), fake.color_name())
        cursor.execute(sql, val)
    
    # Table 4: Products
    for _ in range(num_rows):
        sql = "INSERT INTO test.products (product_name, category, price, stock_quantity) VALUES (%s, %s, %s, %s)"
        val = (fake.word(), fake.word(), round(random.uniform(10, 1000), 2), random.randint(0, 1000))
        cursor.execute(sql, val)
    
    # Table 5: Orders
    for _ in range(num_rows):
        sql = "INSERT INTO test.orders (order_date, customer_name, total_amount, status) VALUES (%s, %s, %s, %s)"
        val = (fake.date_this_decade(), fake.name(), round(random.uniform(100, 5000), 2), random.choice(['Pending', 'Shipped', 'Delivered', 'Cancelled']))
        cursor.execute(sql, val)
    
    # Table 6: Employees
    for _ in range(num_rows):
        sql = "INSERT INTO test.employees (first_name, last_name, hire_date, position, salary) VALUES (%s, %s, %s, %s, %s)"
        val = (fake.first_name(), fake.last_name(), fake.date_between(start_date='-30y', end_date='today'), fake.job(), round(random.uniform(30000, 200000), 2))
        cursor.execute(sql, val)
    
    # Table 7: Departments
    for _ in range(num_rows):
        sql = "INSERT INTO test.departments (department_name, manager_name, budget) VALUES (%s, %s, %s)"
        val = (fake.word(), fake.name(), round(random.uniform(50000, 1000000), 2))
        cursor.execute(sql, val)
    
    # Table 8: Cities
    for _ in range(num_rows):
        sql = "INSERT INTO test.cities (city_name, country, population, area_km2) VALUES (%s, %s, %s, %s)"
        val = (fake.city(), fake.country(), random.randint(10000, 10000000), round(random.uniform(10.0, 1000.0), 2))
        cursor.execute(sql, val)
    
    # Table 9: Countries
    continents = ['Africa', 'Asia', 'Europe', 'North America', 'South America', 'Oceania', 'Antarctica']
    for _ in range(num_rows):
        sql = "INSERT INTO test.countries (country_name, continent, population, gdp_trillions) VALUES (%s, %s, %s, %s)"
        val = (fake.country(), random.choice(continents), random.randint(1000000, 1400000000), round(random.uniform(0.1, 25.0), 2))
        cursor.execute(sql, val)
    
    # Table 10: Books
    for _ in range(num_rows):
        sql = "INSERT INTO test.books (title, author, publish_date, genre, price) VALUES (%s, %s, %s, %s, %s)"
        val = (fake.catch_phrase(), fake.name(), fake.date_between(start_date='-100y', end_date='today'), random.choice(['Fiction', 'Non-fiction', 'Science Fiction', 'Biography', 'History', 'Fantasy']), round(random.uniform(5, 100), 2))
        cursor.execute(sql, val)

    cnx.commit()  # Commit the transaction

    cursor.close()
    cnx.close()
    
    

if __name__ == "__main__":
    # Call the function with the desired number of rows
    insert_data(connections["config1"], 10)
    insert_data(connections["config2"], 10)