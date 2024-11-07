import onyx.board
import itertools
import collections

# type Piece = str
# type Space = str

class Placement:
    def __init__(self, placements: dict[str, list[str]]):
        self.placements = placements

    def do_move(self, state: "OnyxState"):
        for space, pieces in self.placements.items():
            state.place_piece(space, *pieces)
        state.suffocate_neighbors(*self.placements.keys())

class OnyxState:
    def __init__(self, board: onyx.board.Graph):
        self.board = board
        self.pieces: dict[str, list] = {space: [] for space in board.nodes}
        self.ply = 0

    def place_piece(self, space: str, *pieces: str):
        self.pieces[space].extend(pieces)

    def suffocate_neighbors(self, *spaces: str):
        should_suffocate = set()
        for space in spaces:
            for adjacency in self.board.connections(space):
                if self._should_suffocate(adjacency):
                    should_suffocate.add(adjacency)
        for adjacency in should_suffocate - set(spaces):
            self.pieces[adjacency] = []

    def _count_neighbors(self, space: str) -> collections.Counter[str]:
        return collections.Counter(itertools.chain.from_iterable(
            self.pieces[neighbor]
            for neighbor in self.board.connections(space)
        ))

    def _should_suffocate(self, space: str) -> bool:
        return not all(
            self._is_color_allowed(space, color)
            for color in self.pieces[space]
        )

    def _is_color_allowed(self, space: str, color: str) -> bool:
        neighbors = self._count_neighbors(space)
        neighbors.pop(color, None)
        return sum(neighbors.values()) < 3

    def get_owners(self) -> dict[str, set[str]]:
        owners = {space: set(pieces) for space, pieces in self.pieces.items()}
        changed = True
        while changed:
            changed = False
            new_owners = {
                space: previous_owners | set(itertools.chain.from_iterable(
                    owners[neighbor]
                    for neighbor in self.board.connections(space)
                ))
                if self.pieces[space] == []
                else previous_owners # space is occupied
                for space, previous_owners in owners.items()
            }
            changed = new_owners != owners
            owners = new_owners
        return owners

    def scores_by_color(self) -> collections.Counter[str]:
        return collections.Counter(itertools.chain.from_iterable(self.get_owners().values()))
