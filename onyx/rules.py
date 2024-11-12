import collections
import itertools
import typing

import onyx.board


class Placement:
    def __init__(self, placements: dict[str, list[str]]):
        self.placements = placements

    def do_move(self, state: "OnyxState"):
        for space, pieces in self.placements.items():
            state.place_piece(space, pieces)
        state.suffocate_neighbors(*self.placements.keys())
        state.ply += 1

    def is_legal(self, state: "OnyxState") -> bool:
        playable_colors = state.get_playable_colors()

        # test legality of colors
        for space, pieces in self.placements.items():
            if not all(
                state._is_color_allowed(space, color) and color in playable_colors
                for color in pieces
            ):
                return False
        
        # test legality of distribution
        if len(self.placements) not in [1, 2]:
            return False

        if len(self.placements) == 1:
            pieces = list(self.placements.values())[0]
            if len(pieces) != 2:
                return False
            if len(set(pieces)) != 1:
                return False
        
        if len(self.placements) == 2:
            a, b = list(self.placements.values())
            if len(a) != 1 or len(b) != 1:
                return False
            if len({a[0], b[0]}) != 2:
                return False

        return True


class OnyxState:
    def __init__(
        self,
        board: onyx.board.Graph,
        p1_colors=frozenset({"black", "purple"}),
        p2_colors=frozenset({"white", "yellow"}),
    ):
        self.board = board
        self.pieces: dict[str, list] = {space: [] for space in board.nodes}
        self.ply = 0
        self.p1_colors = frozenset(p1_colors)
        self.p2_colors = frozenset(p2_colors)

    def place_piece(self, space: str, pieces: list[str]):
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
        return collections.Counter(
            itertools.chain.from_iterable(
                self.pieces[neighbor] for neighbor in self.board.connections(space)
            )
        )

    def _should_suffocate(self, space: str) -> bool:
        return not all(
            self._is_color_allowed(space, color) for color in self.pieces[space]
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
                space: previous_owners
                | set(
                    itertools.chain.from_iterable(
                        owners[neighbor] for neighbor in self.board.connections(space)
                    )
                )
                if self.pieces[space] == []
                else previous_owners  # space is occupied
                for space, previous_owners in owners.items()
            }
            changed = new_owners != owners
            owners = new_owners
        return owners

    def scores_by_color(self) -> collections.Counter[str]:
        return collections.Counter(
            itertools.chain.from_iterable(self.get_owners().values())
        )

    def get_turn(self) -> typing.Literal[1, 2]:
        if self.ply % 2:
            return 2
        else:
            return 1

    def get_playable_colors(self):
        if self.get_turn() == 1:
            return self.p1_colors
        else:
            return self.p2_colors
