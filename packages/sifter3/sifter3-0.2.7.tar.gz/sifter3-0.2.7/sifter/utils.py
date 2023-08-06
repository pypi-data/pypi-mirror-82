from typing import (
    Text
)


def indent_string(s: Text, num_spaces: int) -> Text:
    add_newline = False
    if s[-1] == '\n':
        add_newline = True
        s = s[:-1]
    s = '\n'.join(num_spaces * ' ' + line for line in s.split('\n'))
    if add_newline:
        s += '\n'
    return s
