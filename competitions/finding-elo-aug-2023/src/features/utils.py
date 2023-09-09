import pandas as pd
from chess.pgn import read_game
from src.features.game import (
    get_game_info,
    get_piece_moves,
    get_checks,
    get_captures,
    get_player_ratings,
)


def pgn_to_dataframe(pgn_file):
    games = []

    # Load PGN
    pgn = open(pgn_file)

    # Iterate over games
    while True:
        game = read_game(pgn)
        if game is None:
            break

        # Extract info
        game_info = get_game_info(game)
        piece_moves = get_piece_moves(game)
        check_counts = get_checks(game)
        capture_counts = get_captures(game)
        player_ratings = get_player_ratings(game)

        # Compile game data
        games.append(
            {
                **game_info,
                **piece_moves,
                **check_counts,
                **capture_counts,
                **player_ratings,
            }
        )

    # Build DataFrame
    return pd.DataFrame(games)
