import math

__all__ = [
    name for name in globals()
    if not name.startswith("_")
    and callable(globals()[name])
]


def show_as_10th_power(num: int, length_to_return_string: int = 2) -> str:
    """
    Docstring for show_as_10th_power
    Convert a number to a string representation in the form of "a*10^b".
    If the number has less digits than length_to_return_string, return it as a string.
    else it returns a tuple (string_Answer, first_digit, power)

    """
    try:
        as_String = str(num)    
        length = len(as_String)
        if length <= length_to_return_string:
            return as_String
        else:
            power = length - 1
            first_digit = as_String[0]
            string_Answer = f"{first_digit}*10^{power}"
            return string_Answer , int(first_digit), int(power)
    except Exception as e:
        return math.floor(math.log10(abs(num))) + 1


def add_Commas(num) -> str:
    """Format a number with commas as thousands separators."""
    try:
        return f"{num:,}"
    except Exception as e:
        return str(num)


def print_tuples(tup):
    for item in tup:
        print(f"item: {item}")
    print(tup)


def get_input_list(prompt:str, type_cast:type = int) -> list:
    user_input = input(prompt)
    input_list = [type_cast(item.strip()) for item in user_input.split(',')]
    return input_list


def bytes_format_string(num_bytes: int, inputsuffix: str = 'B', outputsuffix: str = 'B', show_conversion: bool = False) -> str:
    
    """Convert bytes to a human-readable format. returns a string in the format 'XX.XX SUFFIX'."""
    suffixes = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
    if inputsuffix not in suffixes or outputsuffix not in suffixes:
        raise ValueError("Invalid suffix provided.")
    index = suffixes.index(inputsuffix)
    num_bytes_converted = num_bytes / (1024 ** index)

    for suffix in suffixes[index:]:
        if num_bytes_converted < 1024:
            break
        num_bytes_converted /= 1024

    if outputsuffix in suffixes:
        while suffix != outputsuffix and suffix in suffixes:
            num_bytes_converted *= 1024
            suffix = suffixes[suffixes.index(suffix) - 1]

    if show_conversion:
        print(f"{num_bytes} {inputsuffix} = {num_bytes_converted:.2f} {suffix}")
    return f"{num_bytes_converted:.2f} {suffix}"


def bytes_format_tuple(num_bytes: int, inputsuffix: str = 'B', outputsuffix: str = 'B', show_conversion: bool = False):
    
    """Convert bytes to a human-readable format. returns tuple in format (converted_value, suffix)"""
    suffixes = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
    if inputsuffix not in suffixes or outputsuffix not in suffixes:
        raise ValueError("Invalid suffix provided.")
    index = suffixes.index(inputsuffix)
    num_bytes_converted = num_bytes / (1024 ** index)

    for suffix in suffixes[index:]:
        if num_bytes_converted < 1024:
            break
        num_bytes_converted /= 1024

    if outputsuffix in suffixes:
        while suffix != outputsuffix and suffix in suffixes:
            num_bytes_converted *= 1024
            suffix = suffixes[suffixes.index(suffix) - 1]

    if show_conversion:
        print(f"{num_bytes} {inputsuffix} = {num_bytes_converted:.2f} {suffix}")
    return (num_bytes_converted, suffix)


def duration_format_string(length: int, input_unit: str, output_unit: str, show_conversion: bool = False) -> str:   
    """Convert duration to a human-readable format. returns a string in the format 'XX.XX UNIT'."""
    units_in_seconds = {
        'seconds': 1,
        'minutes': 60,
        'hours': 3600,
        'days': 86400,
        'weeks': 604800,
    }

    if input_unit not in units_in_seconds or output_unit not in units_in_seconds:
        raise ValueError("Invalid time unit provided.")

    length_in_seconds = length * units_in_seconds[input_unit]
    converted_length = length_in_seconds / units_in_seconds[output_unit]

    if show_conversion:
        return f"{length} {input_unit} = {converted_length:.2f} {output_unit}"
    return f"{converted_length:.2f} {output_unit}"
    

def duration_format_tuple(length: int, input_unit: str, output_unit: str, show_conversion: bool = False):   
    """Convert duration to a human-readable format. returns tuple in format (converted_value, unit)"""
    units_in_seconds = {
        'seconds': 1,
        'minutes': 60,
        'hours': 3600,
        'days': 86400,
        'weeks': 604800,
    }

    if input_unit not in units_in_seconds or output_unit not in units_in_seconds:
        raise ValueError("Invalid time unit provided.")

    length_in_seconds = length * units_in_seconds[input_unit]
    converted_length = length_in_seconds / units_in_seconds[output_unit]

    if show_conversion:
        print(f"{length} {input_unit} = {converted_length:.2f} {output_unit}")
    return (converted_length, output_unit)

