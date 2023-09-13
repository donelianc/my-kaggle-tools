import pandas as pd
from chess.pgn import read_game
from src.features.game import (
    get_captures,
    get_castling,
    get_checks,
    get_game_info,
    get_piece_moves,
    get_promorions,
)
from src.features.opening import get_opening_features
from src.features.players import get_player_ratings


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
        player_ratings = get_player_ratings(game)
        game_info = get_game_info(game)
        piece_moves = get_piece_moves(game)
        check_counts = get_checks(game)
        capture_counts = get_captures(game)
        promotion_counts = get_promorions(game)
        castling_counts = get_castling(game)
        opening_features = get_opening_features(game)

        # Compile game data
        games.append(
            {
                **player_ratings,
                **game_info,
                **piece_moves,
                **check_counts,
                **capture_counts,
                **promotion_counts,
                **castling_counts,
                **opening_features,
            }
        )

    # Build DataFrame
    df = pd.DataFrame(games)
    df.insert(
        loc=0,
        column="rating_diff",
        value=df["wp_rating"].astype(int) - df["bp_rating"].astype(int),
    )

    return df
