def get_game_info(game):
    # Get total moves from perspective of white
    total_moves = len(list(game.mainline_moves()))

    # Initialize variables
    white_moves = None
    black_moves = None
    white_won = None

    # Determine outcome
    result = game.headers["Result"]
    if result == "1-0":
        white_won = True
    elif result == "0-1":
        white_won = False

    # Calculate white moves
    white_moves = (total_moves // 2) + (total_moves % 2)

    # Calculate black moves based on parity and outcome
    if white_won is None:
        if total_moves % 2 != 0:
            black_moves = white_moves - 1
        else:
            black_moves = white_moves
    elif white_won:
        black_moves = white_moves - 1
    else:
        black_moves = white_moves

    return {
        "result": result,
        "total_moves": total_moves,
        "wp_total_moves": white_moves,
        "bp_total_moves": black_moves,
    }


def get_piece_moves(game):
    """Track number of moves by piece type and player"""

    # Initialize count for each piece
    cols = ["P", "N", "B", "R", "Q", "K"]
    wp_moves = {col: 0 for col in cols}
    bp_moves = {col: 0 for col in cols}

    # Tally moves by piece based on turn
    board = game.board()
    for move in game.mainline_moves():
        piece = board.piece_at(move.from_square).symbol().upper()
        if board.turn:
            wp_moves[piece] += 1
        else:
            bp_moves[piece] += 1
        board.push(move)

    # Build columns for dataframe
    df_moves = {}
    for col in cols:
        df_moves[f"wp_total_{col}_moves"] = wp_moves[col]
        df_moves[f"bp_total_{col}_moves"] = bp_moves[col]

    return df_moves


def get_checks(game):
    """Count checks performed by each player"""

    # Initialize counters
    wp_checks = 0
    bp_checks = 0

    # Iterate through moves
    board = game.board()
    for move in game.mainline_moves():
        # Make move and continue
        board.push(move)

        # Check if move is a check
        if board.is_check():
            if board.turn:
                wp_checks += 1
            else:
                bp_checks += 1

    # checks are mixed on purpose becase
    # the way how .turn and .is_check() works
    return {"wp_total_checks": bp_checks, "bp_total_checks": wp_checks}


def get_captures(game):
    # Initialize counters
    wp_captures = 0
    bp_captures = 0

    # Iterate through moves
    board = game.board()
    for move in game.mainline_moves():
        # Check if capture occurred
        if board.is_capture(move):
            if board.turn:
                wp_captures += 1
            else:
                bp_captures += 1

        board.push(move)

    return {"wp_total_captures": wp_captures, "bp_total_captures": bp_captures}


def get_promotions(game):
    """Count number of promotions by each player"""

    # Initialize counters
    wp_promotions = 0
    bp_promotions = 0

    # Iterate through moves
    board = game.board()
    for move in game.mainline_moves():
        # Check if promotion occurred
        if move.promotion is not None:
            if board.turn:
                wp_promotions += 1
            else:
                bp_promotions += 1

        board.push(move)

    return {
        "wp_total_promotions": wp_promotions,
        "bp_total_promotions": bp_promotions,
    }


def get_castling(game):
    """Count number of castling moves by each player"""

    # Initialize counters
    wp_castles = False
    bp_castles = False

    # Iterate through moves
    board = game.board()
    for move in game.mainline_moves():
        # Check if castling occurred
        if move in board.generate_castling_moves():
            if board.turn:
                wp_castles = True
            else:
                bp_castles = True

        board.push(move)

    return {
        "wp_bool_castles": wp_castles,
        "bp_bool_castles": bp_castles,
    }
