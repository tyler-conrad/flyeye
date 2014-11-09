import fileinput

from model.node import Node


def tree():
    max_depth = 0
    root = Node(name='/', path='/', parent=None)
    for path in fileinput.input():
        current = root
        name_list = path.split('/')[1:]
        len_name_list = len(name_list)
        max_depth = max(len_name_list, max_depth)
        for name in name_list:
            current = current.setdefault(name, path, current)
    return root, max_depth