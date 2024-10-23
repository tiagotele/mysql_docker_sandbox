import time
from typing import List, Tuple, Dict

from queries import run_query, QUERIES_FIRST_PHASE, TOP_TABLES
from parallel_query import execute_queries_in_parallel
from connector_settings import connections


def print_with_indent(message: str, indent_level=0):
    indent = "    " * indent_level
    print("\n".join(f"{indent}{line}" for line in message.split("\n")) )


def join_tuple_elements(t):
    return ".".join(t)


def compare_lists(
    source_list: List[Tuple] = None,
    destiny_list: List[Tuple] = None,
    source_name: str = "blue",
    destiny_name: str = "green"
) -> str:
    source_list = source_list or []
    destiny_list = destiny_list or []
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
    output_content = f"{source_name},{destiny_name},result\n" + "\n".join(
        f"{item[0]},{item[1]},{item[2]}" for item in output
    )
    return output_content


def fetch_list_from_set(current_set):
    return list(map(lambda x: x[0], current_set))


def fetch_dict_from_set(current_set):
    a = list(map(lambda x: {x[0]: x[1]}, current_set))
    return sorted(a, key=lambda d: next(iter(d)))


def extract_dict_from_list(l: set):
    output = {}
    for i in l:
        output[i[0]] = i[1]
    return output


def compare_dicts(
        dict_a: dict, dict_b: dict, source_name: str = "blue", destiny_name: str = "green"
) -> str:
    result = f"key,{source_name},{destiny_name},result\n"
    all_keys = dict_a.keys() | dict_b.keys()  # Union of both key sets
    result += "\n".join([
        f'{key},{dict_a.get(key, "N/A")},{dict_b.get(key, "N/A")},{"equal" if dict_a.get(key) == dict_b.get(key) else "different"}'
        for key in all_keys
    ])
    return result


def tuples_list_are_equal(l1=None, l2=None):
    return set(l1) == set(l2)


def compare_output_general_phase(output_src: dict, output_dest: dict, show_diff: bool):
    all_keys = set(output_src.keys()).union(set(output_dest.keys()))
    for key in sorted(all_keys):
        if tuples_list_are_equal(output_src[key], output_dest[key]):
            print(f"{key} are igual")
        else:
            print(f"{key} are different")

        if show_diff:
            # If are key value
            if key in ["QUERY_02_VARIABLES", "QUERY_11_LIST_USERS_AND_HOSTS"]:
                source_dict = extract_dict_from_list(set(output_src[key]))
                destiny_dict = extract_dict_from_list(set(output_dest[key]))
                print_with_indent(compare_dicts(source_dict, destiny_dict), 1)
            # If elements are just list
            else:
                print_with_indent(
                    compare_lists(
                        source_list=output_src[key], destiny_list=output_dest[key]
                    ),
                    1,
                )


def parser_tuples_to_str(d: dict):
    result = {}
    for k, v in d.items():
        result[k] = [(tuple(str(item) for item in tpl)) for tpl in v]
    return result

def query_and_show_result(query_src:dict, query_dest:dict, connection_src:dict, connection_dest:dict) -> None:
    output_src, output_dest = execute_queries_in_parallel(
        query_src,
        query_dest,
        connection_src,
        connection_dest
    )

    general_data_source = {name: output for name, query, output in sorted(output_src)}
    general_data_destiny = {name: output for name, query, output in sorted(output_dest)}

    general_data_source = parser_tuples_to_str(general_data_source)
    general_data_destiny = parser_tuples_to_str(general_data_destiny)
    compare_output_general_phase(
        output_src=general_data_source, output_dest=general_data_destiny, show_diff=True
    )


if __name__ == "__main__":

    # FIRST PHASE
    query_and_show_result(QUERIES_FIRST_PHASE, QUERIES_FIRST_PHASE, connections["config1"], connections["config2"])

    top_tables_src = run_query(connections["config1"], "TOP_TABLES", TOP_TABLES)
    top_tables_dest = run_query(connections["config2"], "TOP_TABLES", TOP_TABLES)

    top_queries_dict_src = {f"{schema}.{table}": f"SELECT COUNT(1) FROM {schema}.{table};" for schema, table in
                            top_tables_src[2]}
    top_queries_dict_dest = {f"{schema}.{table}": f"SELECT COUNT(1) FROM {schema}.{table};" for schema, table in
                             top_tables_dest[2]}

    # SECOND PHASE
    query_and_show_result(top_queries_dict_src, top_queries_dict_dest, connections["config1"], connections["config2"])