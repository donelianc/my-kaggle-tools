import pandas as pd
from chess.pgn import read_game
from src.features.game import (
    get_game_info,
    get_piece_moves,
    get_checks,
    get_captures,
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
                **player_ratings,
                **game_info,
                **piece_moves,
                **check_counts,
                **capture_counts,
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


# Functions to extract key data from each game
def get_player_ratings(game):
    """Get player Elo ratings from PGN headers"""
    white_rating = game.headers["WhiteElo"]
    black_rating = game.headers["BlackElo"]

    return {"wp_rating": white_rating, "bp_rating": black_rating}
