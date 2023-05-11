import textwrap

def insert_newlines_char(string, length):
    words = string.split()
    lines = []
    current_line = ""
    for word in words:
        if len(current_line + word) + 1 > length:
            lines.append(current_line.strip())
            current_line = word + " "
        else:
            current_line += word + " "
    if current_line:
        lines.append(current_line.strip())
    return "\n".join(lines)

def newlines_char2(string, length):
    words = string.split('-')
    lines = []
    current_line = ""
    for word in words:
        if len(current_line + word) + 1 > length:
            lines.append(current_line.strip())
            current_line = word + "-"
        else:
            current_line += word + "-"
    if current_line:
        lines.append(current_line.rstrip(current_line[-1]))
    return "\n".join(lines)

def inser_newlines_char4(string, length):
    new_string = ""
    lines = textwrap.wrap(string, width=length)
    for line in lines:
        new_string += line + '\n'
    new_string = new_string.rstrip()
    return new_string
    
def insert_newlines_char3(string, length):
    #string = string.strip()
    words = string.split('/')
    lines = []
    current_line = ""
    for word in words:
        if len(current_line + word) + 1 > length:
            lines.append(current_line.strip())
        current_line = word + "/"
    if current_line:
        lines.append(current_line.rstrip(current_line[-1]))
    return "\n".join(lines)
