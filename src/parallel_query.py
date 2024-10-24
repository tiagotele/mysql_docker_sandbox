from concurrent.futures import ThreadPoolExecutor, as_completed
from queries import run_query

MAX_WORKERS = 32


def run_completed(futures):
    result = []
    for future in as_completed(futures):
        table = futures[future]
        try:
            data = future.result(timeout=10)
            result.append(data)
        except Exception as exc:
            print(f"Query: {table} generated an exception: {exc}")
    return result


def execute_queries_in_parallel(
    queries_src: dict = None,
    queries_dest: dict = None,
    config_src: dict = None,
    config_dest: dict = None,
):
    print("Starting queries")
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        future_to_table_src = {
            executor.submit(run_query, config_src, name, query): (name, query)
            for name, query in queries_src.items()
        }
        future_to_table_dest = {
            executor.submit(run_query, config_dest, name, query): (name, query)
            for name, query in queries_dest.items()
        }

        output_src = run_completed(future_to_table_src)
        output_dest = run_completed(future_to_table_dest)
    return output_src, output_dest
