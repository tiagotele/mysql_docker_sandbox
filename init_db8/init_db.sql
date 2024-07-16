-- Create database and use it
CREATE DATABASE test;
USE test;

-- Create the first table
CREATE TABLE testtab (
    id INTEGER AUTO_INCREMENT,
    name TEXT,
    PRIMARY KEY (id)
) COMMENT='this is my test table';

INSERT INTO testtab (name) VALUES ('Fulano'), ('Sicrano'), ('Beltrano'), ('Zicrano');

-- Create the second table
CREATE TABLE employees (
    employee_id INTEGER AUTO_INCREMENT,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    department VARCHAR(50),
    salary DECIMAL(10, 2),
    PRIMARY KEY (employee_id)
) COMMENT='this is the employees table';

INSERT INTO employees (first_name, last_name, department, salary) VALUES
('John', 'Doe', 'Engineering', 60000.00),
('Jane', 'Smith', 'Marketing', 55000.00),
('Chris', 'Davis', 'Finance', 70000.00);

-- Create the third table
CREATE TABLE products (
    product_id INTEGER AUTO_INCREMENT,
    product_name VARCHAR(100),
    category VARCHAR(50),
    price DECIMAL(10, 2),
    stock_quantity INTEGER,
    PRIMARY KEY (product_id)
) COMMENT='this is the products table';

INSERT INTO products (product_name, category, price, stock_quantity) VALUES
('Laptop', 'Electronics', 1000.00, 50),
('Smartphone', 'Electronics', 700.00, 150),
('Headphones', 'Accessories', 50.00, 300),
('Charger', 'Accessories', 20.00, 500);

-- PERMISSION TO ROOT
GRANT ALL PRIVILEGES ON *.* TO 'root'@'%';
FLUSH PRIVILEGES;