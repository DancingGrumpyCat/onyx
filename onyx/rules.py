import onyx.board
import itertools
import collections

# type Piece = str
# type Space = str

class OnyxState:
    def __init__(self, board: onyx.board.Graph):
        self.board = board
        self.pieces: dict[str, list] = {space: [] for space in board.nodes}
        self.ply = 0

    def place_piece(self, space: str, *pieces: str):
        self.pieces[space].extend(pieces)
        self._suffocate_neighbors(space)

    def _suffocate_neighbors(self, space: str):
        should_suffocate = set()
        for adjacency in self.board.connections(space):
            if self._should_suffocate(adjacency):
                should_suffocate.add(adjacency)
        if self._should_suffocate(space):
            should_suffocate.add(space)
        for adjacency in should_suffocate:
            self.pieces[adjacency] = []

    def _count_neighbors(self, space: str) -> collections.Counter[str]:
        return collections.Counter(itertools.chain.from_iterable(
            self.pieces[neighbor]
            for neighbor in self.board.connections(space)
        ))

    def _should_suffocate(self, space: str) -> bool:
        if self.pieces[space] == []:
            return False
        my_piece_type = self.pieces[space][-1]
        neighbors = self._count_neighbors(space)
        neighbors.pop(my_piece_type, None)
        return sum(neighbors.values()) >= 3