import onyx.board as ob

def test_chess_squares():
    board = ob.chess_like_board(size=2)

    assert board.nodes == {
        "a1", "a2",
        "b1", "b2",
    }


def test_chess_adjacencies():
    board = ob.chess_like_board(size=2)

    assert board.edges == {
        frozenset({"a1", "a2"}),
        frozenset({"a1", "b2"}),
        frozenset({"a1", "b1"}),
        frozenset({"a2", "b1"}),
        frozenset({"a2", "b2"}),
        frozenset({"b1", "b2"}),
    }
