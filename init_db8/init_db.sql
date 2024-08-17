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
    phone_number VARCHAR(30)
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

CREATE DATABASE test2;
USE test2;

-- Drop tables if they already exist
DROP TABLE IF EXISTS people, companies, cars, products, orders, employees, departments, cities, countries, books;

-- Table 1: People
CREATE TABLE people (
    id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    birth_date DATE,
    email VARCHAR(100),
    phone_number VARCHAR(30)
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

-- PERMISSION TO ROOT
GRANT ALL PRIVILEGES ON *.* TO 'root'@'%';
FLUSH PRIVILEGES;