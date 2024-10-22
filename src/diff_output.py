from parallel import compare_output_general_phase

output_source = {
    "QUERY_01_VERSIONS": [("5.7.41",)],
    "QUERY_02_VARIABLES": [
        ("explicit_defaults_for_timestamp", "OFF"),
        ("slave_rows_search_algorithms", "TABLE_SCAN,INDEX_SCAN"),
        ("innodb_open_files", "4000"),
        ("innodb_optimize_fulltext_only", "OFF"),
    ],
    "QUERY_03_SCHEMAS_LIST": [
        ("information_schema",),
        ("mysql",),
        ("performance_schema",),
        ("sys",),
        ("test",),
        ("test2",),
    ],
    "QUERY_04_LIST_TABLES": [
        ("people",),
        ("books",),
    ],
    "QUERY_06_LIST_CONSTRAINTS": [],
    "QUERY_07_LIST_INDEXES": [],
    "QUERY_08_LIST_PARTITIONS": [],
    "QUERY_09_LIST_STORED_PROCEDURES": [],
    "QUERY_10_LIST_TRIGGERS": [
        ("sys_config_insert_set_user", "INSERT", "sys_config"),
        ("sys_config_update_set_user", "UPDATE", "sys_config"),
    ],
    "QUERY_11_LIST_USERS_AND_HOSTS": [
        ("root", "%"),
        ("healthchecker", "localhost"),
        ("mysql.session", "localhost"),
        ("mysql.sys", "localhost"),
        ("root", "localhost"),
    ],
    "QUERY_12_LIST_USERS_AND_ITS_PERMISSIONS": [
        ("root",),
        ("healthchecker",),
        ("mysql.session",),
        ("mysql.sys",),
        ("root",),
    ],
}
output_destiny = {
    "QUERY_01_VERSIONS": [("8.3.0",)],
    "QUERY_02_VARIABLES": [
        ("explicit_defaults_for_timestamp", "ON"),
        ("innodb_open_files", "4000"),
    ],
    "QUERY_03_SCHEMAS_LIST": [
        ("information_schema",),
        ("mysql",),
        ("performance_schema",),
        ("sys",),
        ("test",),
        ("test2",),
    ],
    "QUERY_04_LIST_TABLES": [
        ("people",),
        ("books2",),
    ],
    "QUERY_06_LIST_CONSTRAINTS": [],
    "QUERY_07_LIST_INDEXES": [],
    "QUERY_08_LIST_PARTITIONS": [],
    "QUERY_09_LIST_STORED_PROCEDURES": [],
    "QUERY_10_LIST_TRIGGERS": [
        ("sys_config_insert_set_user", "INSERT", "sys_config"),
        ("sys_config_update_set_user", "UPDATE", "sys_config"),
    ],
    "QUERY_11_LIST_USERS_AND_HOSTS": [
        ("root", "%"),
        ("mysql.infoschema", "localhost"),
        ("mysql.session", "localhost"),
        ("mysql.sys", "localhost"),
        ("root", "localhost"),
    ],
    "QUERY_12_LIST_USERS_AND_ITS_PERMISSIONS": [
        ("root",),
        ("mysql.infoschema",),
        ("mysql.session",),
        ("mysql.sys",),
        ("root",),
    ],
}



if __name__ == "__main__":
    compare_output_general_phase(
        output_src=output_source, output_dest=output_destiny, show_diff=True
    )
