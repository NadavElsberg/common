import time

__all__ = [
    name for name in globals()
    if not name.startswith("_")
    and callable(globals()[name])
]


def countTime(func):
    """Decorator to measure the execution time of a function."""
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Function '{func.__name__}' executed in {end_time - start_time:.6f} seconds.")
        return result
    return wrapper


def printNoNewLine(*args, **kwargs):
    """Prints the given arguments without adding a newline at the end."""
    print(*args, end='', **kwargs)
    print("hii!")