import onyx.rules as rules
import onyx.board as ob

def test_place_piece():
    board = rules.OnyxState(ob.chess_like_board(size=2))
    rules.Placement({
        "a1": ["white"]
    }).do_move(board)
    assert board.pieces == {
        "a1": ["white"],
        "a2": [],
        "b1": [],
        "b2": [],
    }

def test_suffocate_neighbors_1():
    board = rules.OnyxState(ob.chess_like_board(size=2))
    rules.Placement({
        "a1": ["white"]
    }).do_move(board)
    rules.Placement({
        "b1": ["black"],
        "a2": ["black"],
        "b2": ["black"],
    }).do_move(board)
    assert board.pieces == {
        "a1": [],
        "a2": ["black"],
        "b1": ["black"],
        "b2": ["black"],
    }

def test_suffocate_neighbors_2():
    board = rules.OnyxState(ob.chess_like_board(size=2))
    rules.Placement({
        "a1": ["white"],
    }).do_move(board)
    rules.Placement({
        "b2": ["purple"],
    }).do_move(board)
    rules.Placement({
        "a2": ["black", "black"],
    }).do_move(board)
    assert board.pieces == {
        "a1": [],
        "a2": ["black", "black"],
        "b1": [],
        "b2": [],
    }

def test_basic_scoring_1():
    board = rules.OnyxState(ob.chess_like_board(size=2))
    rules.Placement({
        "a1": ["white"],
    }).do_move(board)
    rules.Placement({
        "b2": ["purple"],
    }).do_move(board)
    rules.Placement({
        "a2": ["black", "black"],
    }).do_move(board)
    assert board.get_owners() == {
        "a1": {"black"},
        "a2": {"black"},
        "b1": {"black"},
        "b2": {"black"},
    }
    assert board.scores_by_color() == {
        "black": 4,
    }

def test_basic_scoring_2():
    board = rules.OnyxState(ob.chess_like_board(size=4))

    # - b b - 4
    # - - b p 3
    # w w - - 2
    # - w - Y 1
    # a b c d

    rules.Placement({
        "b1": ["white"],
        "a2": ["white"],
        "b2": ["white"],
        "d1": ["yellow", "yellow"],
        "b4": ["black"],
        "c4": ["black"],
        "c3": ["black"],
        "d3": ["purple"],
    }).do_move(board)

    assert board.get_owners() == {
        "a1": {"white"},
        "b1": {"white"},
        "c1": {"white", "yellow", "black", "purple"},
        "d1": {"yellow"},
        "a2": {"white"},
        "b2": {"white"},
        "c2": {"white", "yellow", "black", "purple"},
        "d2": {"white", "yellow", "black", "purple"},
        "a3": {"white", "yellow", "black", "purple"},
        "b3": {"white", "yellow", "black", "purple"},
        "c3": {"black"},
        "d3": {"purple"},
        "a4": {"white", "yellow", "black", "purple"},
        "b4": {"black"},
        "c4": {"black"},
        "d4": {"black", "purple"},
    }

    assert board.scores_by_color() == {
        "white": 10,
        "yellow": 7,
        "black": 10,
        "purple": 8,
    }
