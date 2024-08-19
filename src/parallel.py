import time
from concurrent.futures import ThreadPoolExecutor, as_completed

from queries import run_query, QUERIES_FIRST_PHASE
from parallel_query import execute_queries_in_parallel
from connector_settings import connections


if __name__ == "__main__":
    s = time.time()
    # for query in QUERIES_FIRST_PHASE:
    #     print(query)
    output = execute_queries_in_parallel(
        QUERIES_FIRST_PHASE,
        QUERIES_FIRST_PHASE,
        connections["config1"],
        connections["config2"],
    )
    e = time.time()
    total_time = e - s
    print("-----------")
    print(f"Total time = {total_time:.3f}")
    print(output[0])
    print("-----------")
    print(output[1])
