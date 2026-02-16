import time

__all__ = [
    name for name in globals()
    if not name.startswith("_")
    and callable(globals()[name])
]

def baseWrapper(func):
    """A base wrapper function that can be used as a template for other wrappers."""
    def wrapper(*args, **kwargs):
        # Pre-processing code can go here (e.g. logging, input validation)
        print(f"Calling function '{func.__name__}' with args: {args} and kwargs: {kwargs}")
        
        # Call the original function
        result = func(*args, **kwargs)
        
        # Post-processing code can go here (e.g. logging, modifying the result)
        print(f"Function '{func.__name__}' returned: {result}")
        
        return result
    return wrapper


def countTime(func):
    """Decorator to measure the execution time of a function."""
    def wrapper(*args, **kwargs):
        start_time = time.time()
        end_time = time.time()
        result = func(*args, **kwargs)
        print(f"Function '{func.__name__}' executed in {end_time - start_time:.6f} seconds.")
        return result
    return wrapper