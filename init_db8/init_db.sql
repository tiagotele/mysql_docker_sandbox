-- Use the 'test' schema
CREATE DATABASE test;
USE test;

-- Drop tables if they already exist
DROP TABLE IF EXISTS people, companies, cars, products, orders, employees, departments, cities, countries, books;

-- Table 1: People
CREATE TABLE people (
    id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    birth_date DATE,
    email VARCHAR(100),
    phone_number VARCHAR(15)
);

-- Table 2: Companies
CREATE TABLE companies (
    id INT AUTO_INCREMENT PRIMARY KEY,
    company_name VARCHAR(100),
    founded_date DATE,
    industry VARCHAR(50),
    ceo_name VARCHAR(100)
);

-- Table 3: Cars
CREATE TABLE cars (
    id INT AUTO_INCREMENT PRIMARY KEY,
    make VARCHAR(50),
    model VARCHAR(50),
    year INT,
    price DECIMAL(10,2),
    color VARCHAR(20)
);

-- Table 4: Products
CREATE TABLE products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    product_name VARCHAR(100),
    category VARCHAR(50),
    price DECIMAL(10,2),
    stock_quantity INT
);

-- Table 5: Orders
CREATE TABLE orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_date DATE,
    customer_name VARCHAR(100),
    total_amount DECIMAL(10,2),
    status VARCHAR(20)
);

-- Table 6: Employees
CREATE TABLE employees (
    id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    hire_date DATE,
    position VARCHAR(50),
    salary DECIMAL(10,2)
);

-- Table 7: Departments
CREATE TABLE departments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    department_name VARCHAR(100),
    manager_name VARCHAR(100),
    budget DECIMAL(15,2)
);

-- Table 8: Cities
CREATE TABLE cities (
    id INT AUTO_INCREMENT PRIMARY KEY,
    city_name VARCHAR(100),
    country VARCHAR(50),
    population INT,
    area_km2 DECIMAL(10,2)
);

-- Table 9: Countries
CREATE TABLE countries (
    id INT AUTO_INCREMENT PRIMARY KEY,
    country_name VARCHAR(100),
    continent VARCHAR(50),
    population INT,
    gdp_trillions DECIMAL(15,2)
);

-- Table 10: Books
CREATE TABLE books (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(100),
    author VARCHAR(100),
    publish_date DATE,
    genre VARCHAR(50),
    price DECIMAL(10,2)
);

-- Insert 50 random rows into each table
DELIMITER //

CREATE PROCEDURE insert_random_data()
BEGIN
    -- Insert into People
    INSERT INTO people (first_name, last_name, birth_date, email, phone_number)
    SELECT
        CONCAT('First', FLOOR(1 + (RAND() * 100))),
        CONCAT('Last', FLOOR(1 + (RAND() * 100))),
        CURDATE() - INTERVAL FLOOR(RAND() * 365*30) DAY,
        CONCAT('email', FLOOR(1 + (RAND() * 100)), '@example.com'),
        CONCAT('+1-', FLOOR(RAND() * 999), '-', FLOOR(RAND() * 999), '-', FLOOR(RAND() * 9999))
    FROM
        information_schema.columns
    LIMIT 50;

    -- Insert into Companies
    INSERT INTO companies (company_name, founded_date, industry, ceo_name)
    SELECT
        CONCAT('Company', FLOOR(1 + (RAND() * 100))),
        CURDATE() - INTERVAL FLOOR(RAND() * 365*50) DAY,
        CONCAT('Industry', FLOOR(1 + (RAND() * 10))),
        CONCAT('CEO', FLOOR(1 + (RAND() * 100)))
    FROM
        information_schema.columns
    LIMIT 50;

    -- Insert into Cars
    INSERT INTO cars (make, model, year, price, color)
    SELECT
        CONCAT('Make', FLOOR(1 + (RAND() * 10))),
        CONCAT('Model', FLOOR(1 + (RAND() * 100))),
        FLOOR(1990 + (RAND() * 30)),
        RAND() * 50000,
        CONCAT('Color', FLOOR(1 + (RAND() * 10)))
    FROM
        information_schema.columns
    LIMIT 50;

    -- Insert into Products
    INSERT INTO products (product_name, category, price, stock_quantity)
    SELECT
        CONCAT('Product', FLOOR(1 + (RAND() * 100))),
        CONCAT('Category', FLOOR(1 + (RAND() * 10))),
        RAND() * 1000,
        FLOOR(RAND() * 500)
    FROM
        information_schema.columns
    LIMIT 50;

    -- Insert into Orders
    INSERT INTO orders (order_date, customer_name, total_amount, status)
    SELECT
        CURDATE() - INTERVAL FLOOR(RAND() * 365*2) DAY,
        CONCAT('Customer', FLOOR(1 + (RAND() * 100))),
        RAND() * 10000,
        CASE FLOOR(1 + (RAND() * 4))
            WHEN 1 THEN 'Pending'
            WHEN 2 THEN 'Shipped'
            WHEN 3 THEN 'Delivered'
            ELSE 'Canceled'
        END
    FROM
        information_schema.columns
    LIMIT 50;

    -- Insert into Employees
    INSERT INTO employees (first_name, last_name, hire_date, position, salary)
    SELECT
        CONCAT('First', FLOOR(1 + (RAND() * 100))),
        CONCAT('Last', FLOOR(1 + (RAND() * 100))),
        CURDATE() - INTERVAL FLOOR(RAND() * 365*20) DAY,
        CONCAT('Position', FLOOR(1 + (RAND() * 10))),
        RAND() * 100000
    FROM
        information_schema.columns
    LIMIT 50;

    -- Insert into Departments
    INSERT INTO departments (department_name, manager_name, budget)
    SELECT
        CONCAT('Department', FLOOR(1 + (RAND() * 10))),
        CONCAT('Manager', FLOOR(1 + (RAND() * 100))),
        RAND() * 10000000
    FROM
        information_schema.columns
    LIMIT 50;

    -- Insert into Cities
    INSERT INTO cities (city_name, country, population, area_km2)
    SELECT
        CONCAT('City', FLOOR(1 + (RAND() * 100))),
        CONCAT('Country', FLOOR(1 + (RAND() * 50))),
        FLOOR(RAND() * 1000000),
        RAND() * 1000
    FROM
        information_schema.columns
    LIMIT 50;

    -- Insert into Countries
    INSERT INTO countries (country_name, continent, population, gdp_trillions)
    SELECT
        CONCAT('Country', FLOOR(1 + (RAND() * 100))),
        CASE FLOOR(1 + (RAND() * 6))
            WHEN 1 THEN 'Asia'
            WHEN 2 THEN 'Europe'
            WHEN 3 THEN 'North America'
            WHEN 4 THEN 'South America'
            WHEN 5 THEN 'Africa'
            ELSE 'Oceania'
        END,
        FLOOR(RAND() * 100000000),
        RAND() * 10
    FROM
        information_schema.columns
    LIMIT 50;

    -- Insert into Books
    INSERT INTO books (title, author, publish_date, genre, price)
    SELECT
        CONCAT('Book', FLOOR(1 + (RAND() * 100))),
        CONCAT('Author', FLOOR(1 + (RAND() * 100))),
        CURDATE() - INTERVAL FLOOR(RAND() * 365*100) DAY,
        CONCAT('Genre', FLOOR(1 + (RAND() * 10))),
        RAND() * 100
    FROM
        information_schema.columns
    LIMIT 50;
END//

DELIMITER ;

-- Execute the procedure to insert data
CALL insert_random_data();

-- Clean up by dropping the procedure
DROP PROCEDURE IF EXISTS insert_random_data;