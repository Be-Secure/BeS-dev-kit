def insert_newline_char(string, max_length, delimeter):
    ''' Add new line char (\n) after a given length'''
    if len(string) <= max_length:
        return string
    len_of_str = len(string)
    i = 0
    lines = []
    prev_index = 0
    break_index = 0
    counter = 0
    while i < len_of_str:
        if string[i] == delimeter:
            break_index = i
        if counter == max_length:
            counter = 0
            if break_index <= prev_index:
                lines.append(string[prev_index : i+1].strip())
                prev_index = i + 1
            else:
                lines.append(string[prev_index : break_index+1].strip())
                prev_index = break_index + 1
        if i == len_of_str-1:
            counter = 0
            lines.append(string[prev_index : i+1].strip())
            prev_index = i + 1
        i += 1
        counter += 1
    return "\n".join(lines)