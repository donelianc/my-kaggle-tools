from typing import Dict

from chess.pgn import Game


def get_game_info(game: Game) -> Dict[str, str | int]:
    """
    Extracts general information from a game, such as the total number of moves,
    the result, and the total moves by each player.

    :param game: A chess game object.
    :return: A dictionary containing the extracted information.
    """
    total_moves = len(list(game.mainline_moves()))
    result = game.headers["Result"]
    white_won = None
    if result == "1-0":
        white_won = True
    elif result == "0-1":
        white_won = False

    white_moves = (total_moves // 2) + (total_moves % 2)
    black_moves = white_moves if white_won is None else white_moves - int(white_won)

    return {
        "result": result,
        "total_moves": total_moves,
        "wp_total_moves": white_moves,
        "bp_total_moves": black_moves,
    }


def get_piece_moves(game: Game) -> Dict[str, int]:
    """
    Tracks the number of moves by piece type and player.

    :param game: A chess game object.
    :return: A dictionary containing the total moves by each piece for white
    and black players.
    """
    cols = ["P", "N", "B", "R", "Q", "K"]
    wp_moves = {col: 0 for col in cols}
    bp_moves = {col: 0 for col in cols}
    board = game.board()

    for move in game.mainline_moves():
        piece_entity = board.piece_at(move.from_square)
        if piece_entity:  # Check to ensure a piece exists at the square
            piece = piece_entity.symbol().upper()
            if board.turn:
                wp_moves[piece] += 1
            else:
                bp_moves[piece] += 1
        board.push(move)

    return {f"wp_total_{col}_moves": wp_moves[col] for col in cols} | {
        f"bp_total_{col}_moves": bp_moves[col] for col in cols
    }


def get_checks(game: Game) -> Dict[str, int]:
    """
    Counts the number of checks performed by each player.

    :param game: A chess game object.
    :return: A dictionary containing the total number of checks by white
    and black players.
    """
    wp_checks = bp_checks = 0
    board = game.board()

    for move in game.mainline_moves():
        board.push(move)
        if board.is_check():
            wp_checks += board.turn
            bp_checks += not board.turn

    return {"wp_total_checks": bp_checks, "bp_total_checks": wp_checks}


def get_captures(game: Game) -> Dict[str, int]:
    """
    Counts the number of captures made by each player.

    :param game: A chess game object.
    :return: A dictionary containing the total number of captures by
    white and black players.
    """
    wp_captures = bp_captures = 0
    board = game.board()

    for move in game.mainline_moves():
        if board.is_capture(move):
            wp_captures += board.turn
            bp_captures += not board.turn
        board.push(move)

    return {"wp_total_captures": wp_captures, "bp_total_captures": bp_captures}


def get_promotions(game: Game) -> Dict[str, int]:
    """
    Counts the number of promotions made by each player.

    :param game: A chess game object.
    :return: A dictionary containing the total number of promotions by
    white and black players.
    """
    wp_promotions = bp_promotions = 0
    board = game.board()

    for move in game.mainline_moves():
        if move.promotion is not None:
            wp_promotions += board.turn
            bp_promotions += not board.turn
        board.push(move)

    return {"wp_total_promotions": wp_promotions, "bp_total_promotions": bp_promotions}


def get_castling(game: Game) -> Dict[str, bool]:
    """
    Identifies if castling occurred by each player.

    :param game: A chess game object.
    :return: A dictionary indicating whether white and black players castled.
    """
    wp_castles = bp_castles = False
    board = game.board()

    for move in game.mainline_moves():
        if move in board.generate_castling_moves():
            wp_castles |= board.turn
            bp_castles |= not board.turn
        board.push(move)

    return {"wp_bool_castles": wp_castles, "bp_bool_castles": bp_castles}
