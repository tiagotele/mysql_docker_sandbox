import json
import mysql.connector

with open("config.json", "r") as file:
    connection_config = json.load(file)

source_config = connection_config["source"]
target_config = connection_config["target"]

print(source_config)
print(target_config)


def create_connection(host, port, user, password, database):
    return mysql.connector.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        database=database,
    )

conn_source = create_connection(  # mysql.connector.connect ()
    host=source_config["host"],
    port=source_config["port"],
    user=source_config["user"],
    password=source_config["password"],
    database=source_config["database"],
)

conn_target = create_connection(
    host=target_config["host"],
    port=target_config["port"],
    user=target_config["user"],
    password=target_config["password"],
    database=target_config["database"],
)
