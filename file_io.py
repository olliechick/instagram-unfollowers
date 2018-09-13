import ast


def extract_str(filename):
    """returns a (stripped) string from file"""
    try:
        my_file = open_file(filename, 'r')
    except FileNotFoundError:
        return None
    s = my_file.read()
    my_file.close()
    s = s.strip()
    return s


def extract_list(filename):
    """returns a list from file"""
    try:
        my_file = open_file(filename, 'r')
    except FileNotFoundError:
        return None
    s = my_file.read()
    my_file.close()
    sanitised_s = ''
    in_double_quotes = False
    for char in s:
        if char == '"' and in_double_quotes:
            in_double_quotes = False
            sanitised_s += char
        elif char == '"':
            in_double_quotes = True
            sanitised_s += char
        elif char == "'" and in_double_quotes:
            sanitised_s += '\\' + "'"
        else:
            sanitised_s += char
    l = eval(sanitised_s.strip())
    return l


def extract_dict(filename):
    """returns a dictionary from file"""
    try:
        my_file = open_file(filename, 'r')
    except FileNotFoundError:
        return None
    s = my_file.read()
    my_file.close()

    try:
        d = ast.literal_eval(s)
    except ValueError:
        return None

    if isinstance(d, dict):
        return d
    else:
        return None


def write_to_file(filename, contents):
    '''Writes contents to file filename'''
    outfile = open_file(filename, 'w+', encoding="utf-8")
    outfile.write(contents)
    outfile.close()


def open_file(filename, mode, encoding="utf-8", errors='ignore'):
    myfile = open(filename, mode, encoding=encoding, errors=errors)
    return myfile

