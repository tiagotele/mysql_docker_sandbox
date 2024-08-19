from concurrent.futures import ThreadPoolExecutor, as_completed
from queries import run_query

MAX_WORKERS = 32


def run_completed(futures):
    result=[]
    for future in as_completed(futures):
        table = futures[future]
        try:
            data = future.result(timeout=10)
            result.append(data)
            print(f"Done = {data}")
        except Exception as exc:
            print(f"Query: {table} generated an exception: {exc}")
    return result


def execute_queries_in_parallel(
    queries1: list[str] = [],
    queries2: list[str] = [],
    config1: dict = {},
    config2: dict = {},
):
    print("Starting queries")
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        future_to_table1 = {
            executor.submit(run_query, config1, query): query for query in queries1
        }
        future_to_table2 = {
            executor.submit(run_query, config2, query): query for query in queries2
        }

        output1 = run_completed(future_to_table1)
        output2 = run_completed(future_to_table2)
    return output1, output2
