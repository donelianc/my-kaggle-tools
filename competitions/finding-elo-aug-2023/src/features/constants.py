import chess

PAWN_STARTING_SQUARES = {
    chess.WHITE: [
        chess.A2,
        chess.B2,
        chess.C2,
        chess.D2,
        chess.E2,
        chess.F2,
        chess.G2,
        chess.H2,
    ],
    chess.BLACK: [
        chess.A7,
        chess.B7,
        chess.C7,
        chess.D7,
        chess.E7,
        chess.F7,
        chess.G7,
        chess.H7,
    ],
}

KNIGHT_STARTING_SQUARES = {
    chess.WHITE: [chess.B1, chess.G1],
    chess.BLACK: [chess.B8, chess.G8],
}

BISHOP_STARTING_SQUARES = {
    chess.WHITE: [chess.C1, chess.F1],
    chess.BLACK: [chess.C8, chess.F8],
}

ROOK_STARTING_SQUARES = {
    chess.WHITE: [chess.A1, chess.H1],
    chess.BLACK: [chess.A8, chess.H8],
}

QUEEN_STARTING_SQUARES = {chess.WHITE: [chess.D1], chess.BLACK: [chess.D8]}

KING_STARTING_SQUARES = {chess.WHITE: [chess.E1], chess.BLACK: [chess.E8]}

ALL_STARTING_SQUARES = (
    PAWN_STARTING_SQUARES[chess.WHITE]
    + PAWN_STARTING_SQUARES[chess.BLACK]
    + KNIGHT_STARTING_SQUARES[chess.WHITE]
    + KNIGHT_STARTING_SQUARES[chess.BLACK]
    + BISHOP_STARTING_SQUARES[chess.WHITE]
    + BISHOP_STARTING_SQUARES[chess.BLACK]
    + ROOK_STARTING_SQUARES[chess.WHITE]
    + ROOK_STARTING_SQUARES[chess.BLACK]
    + QUEEN_STARTING_SQUARES[chess.WHITE]
    + QUEEN_STARTING_SQUARES[chess.BLACK]
    + KING_STARTING_SQUARES[chess.WHITE]
    + KING_STARTING_SQUARES[chess.BLACK]
)
