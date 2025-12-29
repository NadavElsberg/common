import math

def show_as_10th_power(num: int) -> str:
    try:
        as_String = str(num)    
        length = len(as_String)
        if length <= 10:
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
