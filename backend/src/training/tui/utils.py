def add_linebreaks(string: str, line_length: int) -> str:
    """
    Add linebreaks to a string before words that would break the line

    Args:
        string (str): the string to which we'll add line breaks
        line_length (int): the length of the line

    Returns:
        str: the line with new linebreaks
    """
    idx = line_length
    ret_string = string

    while idx < len(ret_string):
        while ret_string[idx] != ' ':
            idx -= 1

        ret_string = f'{ret_string[:idx]}\n{ret_string[idx:]}'
        idx += line_length+1

    return ret_string