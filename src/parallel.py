import time
from concurrent.futures import ThreadPoolExecutor, as_completed

from queries import run_query, QUERIES_FIRST_PHASE, TOP_TABLES
from parallel_query import execute_queries_in_parallel
from connector_settings import connections


def print_with_indent(message:str, indent_level=0):
    lines = message.split("\n")
    for line in lines:
        indent = "    " * indent_level  # Each indent level adds 4 spaces
        print(f"{indent}{line}")

def join_tuple_elements(t):
    return ".".join(t)

def compare_lists(
    source_list: list = [],
    destiny_list: list = [],
    source_name: str = "blue",
    destiny_name: str = "green",
):
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
    for item in output:
        output_content = output_content + "\n" + item[0] + "," + item[1] + "," + item[2]
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

# key_value diff
def kv_diff(source: list, destiny: list) -> str:
    source_dict = extract_dict_from_list(set(source))
    destiny_dict = extract_dict_from_list(set(destiny))
    return compare_dicts(source_dict, destiny_dict)


def compare_dicts(
    dict_a: dict, dict_b: dict, source_name: str = "blue", destiny_name: str = "green"
) -> str:
    all_keys = set(dict_a.keys()).union(set(dict_b.keys()))
    result = f"key,{source_name},{destiny_name},result"
    for key in all_keys:
        value_a = dict_a.get(key, "N/A")
        value_b = dict_b.get(key, "N/A")
        if value_a == "N/A" or value_b == "N/A":
            status = "different"
        elif value_a == value_b:
            status = "equal"
        else:
            status = "different"
        result = result + "\n"
        result = result + f'"{key}","{value_a}","{value_b}",{status}'
    return result

def show_diff(l1: list = [], l2: list = [], transformation=fetch_list_from_set):
    diff_source_target = set(l1) - set(l2)
    diff_target_source = set(l2) - set(l1)

    if diff_source_target != set():
        print(f"\n\nSource doesn't have this elements:")
        it = transformation(diff_source_target)
        for i in it:
            print(i)

    if diff_target_source != set():
        print(f"\n\nDestiny doesn't have this elements:")
        it = transformation(diff_target_source)
        for i in it:
            print(i)


def tuples_list_are_equal(l1: list = [], l2: list = []) -> bool:
    equal_result = False

    if len(l1) != len(l2):
        return equal_result

    if set(l1) - set(l2) == set() and set(l2) - set(l1) == set():
        equal_result = True
    return equal_result

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


if __name__ == "__main__":
    
    # ################################################################
    # # FIRST PHASE
    # ################################################################
    
    print(f"first phase")
    s = time.time()
    output_src, output_dest = execute_queries_in_parallel(
        QUERIES_FIRST_PHASE,
        QUERIES_FIRST_PHASE,
        connections["config1"],
        connections["config2"],
    )
    e = time.time()
    total_time = e - s
    print("-----------")
    print(f"Total time for queries = {total_time:.3f}")

    general_data_source = {name: output for name, query, output in sorted(output_src)}
    general_data_destiny = {name: output for name, query, output in sorted(output_dest)}

    # ################################################################
    # # FIRST PHASE
    # ################################################################
    compare_output_general_phase(
        output_src=general_data_source, output_dest=general_data_destiny, show_diff=True
    )

    # ################################################################
    # # SECOND PHASE
    # ################################################################
    
    print(f"second phase")
    top_tables_src = run_query(connections["config1"], "TOP_TABLES", TOP_TABLES)
    top_tables_dest = run_query(connections["config2"], "TOP_TABLES", TOP_TABLES)
    
    top_queries_dict_src = {f"{schema}.{table}": f"SELECT COUNT(1) FROM {schema}.{table};" for schema, table in top_tables_src[2]}
    top_queries_dict_dest = {f"{schema}.{table}": f"SELECT COUNT(1) FROM {schema}.{table};" for schema, table in top_tables_dest[2]}
    
    output_src, output_dest = execute_queries_in_parallel(
        top_queries_dict_src,
        top_queries_dict_dest,
        connections["config1"],
        connections["config2"],
    )

    general_data_source = {name: output for name, query, output in sorted(output_src)}
    general_data_destiny = {name: output for name, query, output in sorted(output_dest)}
    
    all_keys = set(general_data_source.keys()).union(set(general_data_destiny.keys()))
    for key in sorted(all_keys):
        print(f"{key}, {general_data_source[key][0][0]}, {general_data_destiny[key][0][0]}")

    