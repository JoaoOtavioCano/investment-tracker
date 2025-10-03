import time
from datetime import datetime


def time_it(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        exec_time = time.time() - start
        print("\n\n-------------------------")
        print(
            f"Execution Time Benchmark:\n\tdate: {datetime.now()}\n\tfunc: {func.__qualname__}\n\texec time: {exec_time}"
        )
        print("\n\n-------------------------\n\n")
        return result

    return wrapper
