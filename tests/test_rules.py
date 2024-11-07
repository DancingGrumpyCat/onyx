import onyx.rules as rules
import onyx.board as ob

def test_place_piece():
    board = rules.OnyxState(ob.chess_like_board(size=2))
    board.place_piece("a1", "white")
    assert board.pieces == {
        "a1": ["white"],
        "a2": [],
        "b1": [],
        "b2": [],
    }

def test_suffocate_neighbors_1():
    board = rules.OnyxState(ob.chess_like_board(size=2))
    board.place_piece("a1", "white")
    board.place_piece("b1", "black")
    board.place_piece("a2", "black")
    board.place_piece("b2", "black")
    assert board.pieces == {
        "a1": [],
        "a2": ["black"],
        "b1": ["black"],
        "b2": ["black"],
    }

def test_suffocate_neighbors_2():
    board = rules.OnyxState(ob.chess_like_board(size=2))
    board.place_piece("a1", "white")
    board.place_piece("a2", "black", "black")
    board.place_piece("b2", "purple")
    assert board.pieces == {
        "a1": [],
        "a2": ["black", "black"],
        "b1": [],
        "b2": [],
    }
