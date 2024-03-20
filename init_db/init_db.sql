create database test;
use test;

CREATE TABLE testtab
(
id INTEGER AUTO_INCREMENT,
name TEXT,
PRIMARY KEY (id)
) COMMENT='this is my test table';

INSERT INTO testtab (name) VALUES ('Fulano'), ('Sicrano'), ('Beltrano');