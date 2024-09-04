import time
from concurrent.futures import ThreadPoolExecutor, as_completed

from queries import run_query, QUERIES_FIRST_PHASE, TOP_TABLES
from parallel_query import execute_queries_in_parallel
from connector_settings import connections


def fetch_list_from_set(current_set):
    return list(map(lambda x: x[0], current_set))


def fetch_dict_from_set(current_set):
    a = list(map(lambda x: {x[0]: x[1]}, current_set))
    return sorted(a, key=lambda d: next(iter(d)))


def compare_dicts(dict_a, dict_b):
    all_keys = set(dict_a.keys()).union(set(dict_b.keys()))
    print(f"table,blue,green,comparator")
    for key in all_keys:
        value_a = dict_a.get(key, "N/A")
        value_b = dict_b.get(key, "N/A")
        if value_a == "N/A" or value_b == "N/A":
            status = "different"
        elif value_a == value_b:
            status = "equal"
        else:
            status = "different"
        print(f'"{key}","{value_a}","{value_b}",{status}')


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


if __name__ == "__main__":
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

    all_keys = set(general_data_source.keys()).union(set(general_data_destiny.keys()))
    for key in sorted(all_keys):
        if tuples_list_are_equal(general_data_source[key], general_data_destiny[key]):
            print(f"{key} are igual")
        else:
            print(f"{key} are different")
            if key in ["QUERY_02_VARIABLES"]:
                show_diff(
                    general_data_source[key],
                    general_data_destiny[key],
                    fetch_dict_from_set,
                )
            else:
                show_diff(
                    general_data_source[key],
                    general_data_destiny[key],
                    fetch_list_from_set,
                )
    
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
