from connector_settings import connections
from parallel_query import execute_queries_in_parallel


# List of tables for which you want to run SELECT COUNT(*)
tables1 = [
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

execute_queries_in_parallel(tables1, tables2, connections["config1"], connections["config2"])