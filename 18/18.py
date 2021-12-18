import re
from itertools import permutations

RIGHT = 1
LEFT = -RIGHT

class Node:
    def __init__(self, parent, parent_side, *args):
        self.value = None
        self.left = self.right = None

        if len(args) == 1:
            self.value = int(args[0])
        if len(args) == 2:
            self.left = args[0]
            args[0].parent = self
            args[0].parent_side = LEFT

            self.right = args[1]
            args[1].parent = self
            args[1].parent_side = RIGHT
        if len(args) > 2:
            raise Exception

        self.parent = parent
        self.parent_side = parent_side
        if parent is not None:
            if parent_side == LEFT:
                parent.left = self
            elif parent_side == RIGHT:
                parent.right = self

    def explode(self):
        left_val, right_val = self.left.value, self.right.value

        # search for next left literal value
        search_node = self
        while search_node.parent_side == LEFT:
            search_node = search_node.parent
        if search_node.parent is not None:
            search_node = search_node.parent.left
            while search_node.value is None:
                search_node = search_node.right
            search_node.value += left_val

        # search for next right literal value
        search_node = self
        while search_node.parent_side == RIGHT:
            search_node = search_node.parent
        if search_node.parent is not None:
            search_node = search_node.parent.right
            while search_node.value is None:
                search_node = search_node.left
            search_node.value += right_val
        
        self.left = self.right = None
        self.value = 0

    def split(self):
        left_val = self.value // 2
        right_val = self.value - left_val
        self.value = None
        self.left = Node(self, LEFT, left_val)
        self.right = Node(self, RIGHT, right_val)

    def find_leftmost_deep_pair(self, depth=0):
        if depth == 4 and self.value is None:
            return self
        if self.value is not None:
            return None
        for node in (self.left, self.right):
            try_this = node.find_leftmost_deep_pair(depth + 1)
            if try_this:
                return try_this
        return None

    def find_leftmost_big_value(self, depth=0):
        if self.value is None:
            for node in (self.left, self.right):
                try_this = node.find_leftmost_big_value(depth + 1)
                if try_this:
                    return try_this
        elif self.value > 9:
            return self
        return None

    def reduce(self):
        while True:
            if (lmdp := self.find_leftmost_deep_pair()):
                lmdp.explode()
                continue
            if (lmbv := self.find_leftmost_big_value()):
                lmbv.split()
                continue
            break
        return self

    def magnitude(self):
        if self.value is not None:
            return self.value
        return 3 * self.left.magnitude() + 2 * self.right.magnitude()

    def __str__(self):
        if self.value is not None:
            return str(self.value)
        return f'[{self.left},{self.right}]'

    def __repr__(self):
        return self.__str__()


def parse(number: str):
    if m := re.fullmatch(r'\d+', number):
        return Node(None, None, int(number))

    if not (m := re.fullmatch(r'\[(.+,.+)\]', number)):
        raise Exception
    
    contents = m.group(1)
    depth = 0
    for i in range(len(contents)):
        match contents[i], depth:
            case '[', _:
                depth += 1
            case ']', _:
                depth -= 1
            case ',', 0:
                return Node(None, None, parse(contents[:i]), parse(contents[i+1:]))


def add(node1, node2):
    return Node(None, None, node1, node2).reduce()


with open('input') as f:
    rows = [row.strip() for row in f.readlines()]

nodes = [parse(row) for row in rows]
node = nodes.pop(0)
while len(nodes) > 0:
    node = Node(None, None, node, nodes.pop(0))
    node.reduce()

print('Part 1:', node.magnitude())

print('Part 2:', max([  add(parse(a), parse(b)).magnitude() 
                        for a, b in permutations(rows, 2)]))
