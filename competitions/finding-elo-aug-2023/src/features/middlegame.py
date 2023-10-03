import chess
from src.features.constants import ALL_STARTING_SQUARES


def identify_middlegame(game):
    """
    Determine the start and end move numbers of the middlegame phase.

    Parameters:
    - game: The chess game object.

    Returns:
    - Tuple with start and end move numbers for middlegame.
    """

    # Initialize some tracking variables
    kings_castled = {"white": False, "black": False}
    pieces_developed = 0
    middlegame_start = None
    middlegame_end = None

    # Traverse through game moves
    board = game.board()
    for move_number, move in enumerate(game.mainline_moves(), 1):
        board.push(move)

        # Check for castling
        if move in board.generate_castling_moves():
            kings_castled["white" if board.turn else "black"] = True

        # Check for piece development (moving from starting position)
        if board.piece_at(move.from_square) in [chess.PAWN, chess.KING]:
            continue  # skip pawns and kings
        if move.from_square in ALL_STARTING_SQUARES:
            pieces_developed += 1

        # Determine start of middlegame
        if not middlegame_start:
            if all(kings_castled.values()) and pieces_developed >= 4:
                middlegame_start = move_number

        # Determine end of middlegame
        # (This is a simple criterion, can be enhanced with more detailed checks)
        if (
            len(board.pieces(chess.QUEEN, chess.WHITE)) == 0
            and len(board.pieces(chess.QUEEN, chess.BLACK)) == 0
            and len(board.piece_map()) < 10
        ):
            middlegame_end = move_number
            break  # exit once we find the end of middlegame

    # If middlegame never really ended (e.g., games that didn't reach an endgame phase)
    if middlegame_start and not middlegame_end:
        middlegame_end = len(list(game.mainline_moves()))

    return (middlegame_start, middlegame_end)
