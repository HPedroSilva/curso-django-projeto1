def is_positive_nuber(value):
    try:
        number_string = float(value)
    except ValueError:
        return False
    return number_string > 0
