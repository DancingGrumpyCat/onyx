import itertools
import string

class Graph:
    def __init__(self):
        self.nodes: set[str] = set()
        self.edges: set[frozenset[str]] = set()

    def is_connected(self, a: str, b: str) -> bool:
        """
        Check whether two nodes, a and b, are connected in this graph.
        """

        return frozenset({a, b}) in self.edges

    def connections(self, node: str) -> set[str]:
        return {
            candidate
            for candidate in self.nodes
            if self.is_connected(candidate, node)
        }

    def add_node(self, node: str):
        self.nodes.add(node)

    def add_edge(self, a: str, b: str):
        self.edges.add(frozenset({a, b}))

# 0-indexed
def chess_square_name(file: int, rank: int) -> str:
    files = string.ascii_lowercase
    return f"{files[file]}{rank+1}"

def is_valid_chess_position(file: int, rank: int, size: int) -> bool:
    return 0 <= file < size and 0 <= rank < size

def chess_adjacencies(file: int, rank: int, size: int):
    for df, dr in itertools.product(range(-1, 2), range(-1, 2)):
        if df == 0 and dr == 0:
            continue
        f, r = file + df, rank + dr
        if not is_valid_chess_position(f, r, size):
            continue
        yield (f, r)

def chess_like_board(size):
    board = Graph()
    for file, rank in itertools.product(range(size), range(size)):
        name = chess_square_name(file, rank)
        board.add_node(name)
        for af, ar in chess_adjacencies(file, rank, size):
            board.add_edge(name, chess_square_name(af, ar))
    return board
