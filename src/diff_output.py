from parallel import tuples_list_are_equal, SHOW_DIFF, show_diff, fetch_dict_from_set, fetch_list_from_set, print_with_indent;

output_source = {'QUERY_01_VERSIONS': [('5.7.41',)],
                 'QUERY_02_VARIABLES': [
                                        ('explicit_defaults_for_timestamp', 'OFF'),
                                        ('slave_rows_search_algorithms', 'TABLE_SCAN,INDEX_SCAN'),
                                        ('innodb_open_files', '4000'), ('innodb_optimize_fulltext_only', 'OFF'),
                                        ],
                 'QUERY_03_SCHEMAS_LIST': [('information_schema',), ('mysql',), ('performance_schema',), ('sys',),
                                           ('test',), ('test2',)],
                 'QUERY_04_LIST_TABLES': [('people',), ('books',),],
                 'QUERY_06_LIST_CONSTRAINTS': [], 'QUERY_07_LIST_INDEXES': [], 'QUERY_08_LIST_PARTITIONS': [],
                 'QUERY_09_LIST_STORED_PROCEDURES': [],
                 'QUERY_10_LIST_TRIGGERS': [('sys_config_insert_set_user', 'INSERT', 'sys_config'),
                                            ('sys_config_update_set_user', 'UPDATE', 'sys_config')],
                 'QUERY_11_LIST_USERS_AND_HOSTS': [('root', '%'), ('healthchecker', 'localhost'),
                                                   ('mysql.session', 'localhost'), ('mysql.sys', 'localhost'),
                                                   ('root', 'localhost')],
                 'QUERY_12_LIST_USERS_AND_ITS_PERMISSIONS': [('root',), ('healthchecker',), ('mysql.session',),
                                                             ('mysql.sys',), ('root',)]}
output_destiny = {'QUERY_01_VERSIONS': [('8.3.0',)],
                  'QUERY_02_VARIABLES': [('explicit_defaults_for_timestamp', 'ON'),
                                        ('innodb_open_files', '4000'),],
                  'QUERY_03_SCHEMAS_LIST': [('information_schema',), ('mysql',), ('performance_schema',), ('sys',),
                                            ('test',), ('test2',)],
                  'QUERY_04_LIST_TABLES': [('people',), ('books2',),],
                  'QUERY_06_LIST_CONSTRAINTS': [], 'QUERY_07_LIST_INDEXES': [], 'QUERY_08_LIST_PARTITIONS': [],
                  'QUERY_09_LIST_STORED_PROCEDURES': [],
                  'QUERY_10_LIST_TRIGGERS': [('sys_config_insert_set_user', 'INSERT', 'sys_config'),
                                             ('sys_config_update_set_user', 'UPDATE', 'sys_config')],
                  'QUERY_11_LIST_USERS_AND_HOSTS': [('root', '%'), ('mysql.infoschema', 'localhost'),
                                                    ('mysql.session', 'localhost'), ('mysql.sys', 'localhost'),
                                                    ('root', 'localhost')],
                  'QUERY_12_LIST_USERS_AND_ITS_PERMISSIONS': [('root',), ('mysql.infoschema',), ('mysql.session',),
                                                              ('mysql.sys',), ('root',)]}

#
# OUTPUT 1
# k1 = v1
# k2 = v2
# k3 = v3
#
# OUTPUT 2
# k1 = v1
# k2 = v1
# k4 = v2
#
# FINAL DIFF
# k1  v1  v2  equals
# k2  v2  v1  diff
# k3  v3  none diff
# k4  none v4 diff


def join_tuple_elements(t):
    return ".".join(t)


def show_tuples_diff(source_list:list = [], destiny_list:list = [], source_name:str = "source", destiny_name:str = "destiny"):
    set_l1 = set(source_list)
    set_l2 = set(destiny_list)

    common = set_l1 & set_l2
    only_in_l1 = set_l1 - set_l2
    only_in_l2 = set_l2 - set_l1

    # Generate the output
    output = []

    # Add common entries
    for item in common:
        output.append((join_tuple_elements(item), join_tuple_elements(item), "Equal"))

    # Add entries only in l1
    for item in only_in_l1:
        output.append((join_tuple_elements(item), "N/A", "Different"))

    # Add entries only in l2
    for item in only_in_l2:
        output.append(("N/A", join_tuple_elements(item), "Different"))

    # Print the output
    output_content = f"{source_name},{destiny_name},result"
    for pair in output:
        output_content = output_content + "\n" + pair[0] + "," +  pair[1] + "," + pair[2]
    return output_content

""" Few are just list others are key value """

def compare_dicts(dict_a, dict_b) -> str:
    all_keys = set(dict_a.keys()).union(set(dict_b.keys()))
    result = f"table,blue,green,comparator"
    for key in all_keys:
        value_a = dict_a.get(key, "N/A")
        value_b = dict_b.get(key, "N/A")
        if value_a == "N/A" or value_b == "N/A":
            status = "different"
        elif value_a == value_b:
            status = "equal"
        else:
            status = "different"
        result = result +  "\n"
        result = result + f'"{key}","{value_a}","{value_b}",{status}'
    return result

def extract_dict_from_list(l: set):
    output = {}
    for i in l:
        output[i[0]] = i[1]
    return output

# key_value diff
def kv_diff(source: list, destiny: list) -> str:
    source_dict = extract_dict_from_list(set(source))
    destiny_dict = extract_dict_from_list(set(destiny))
    return compare_dicts(source_dict, destiny_dict)




all_keys = set(output_source.keys()).union(set(output_destiny.keys()))
for key in sorted(all_keys):
    if tuples_list_are_equal(output_source[key], output_destiny[key]):
        print(f"{key} are igual")
    else:
        print(f"{key} are different")
        # If are key value
        if key in ["QUERY_02_VARIABLES", "QUERY_11_LIST_USERS_AND_HOSTS"]:
            if SHOW_DIFF:
                source_dict = extract_dict_from_list(set(output_source[key]))
                destiny_dict = extract_dict_from_list(set(output_destiny[key]))
                print_with_indent(compare_dicts(source_dict, destiny_dict), 1)
        # If elements are just list
        else:
            if SHOW_DIFF:
                print_with_indent(show_tuples_diff(source_list=output_source[key], destiny_list=output_destiny[key]), 1)
                # show_diff(
                #     output_source[key],
                #     output_destiny[key],
                #     fetch_list_from_set
                # )
