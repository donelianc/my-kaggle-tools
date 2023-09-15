import os
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
from src.features.utils import count_games_in_pgn
from tqdm import tqdm


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


def new_pgn_to_dataframe(
    pgn_file, save_interval=100, save_location="./data/interim/output.csv"
):
    games = []

    # Check if the save_location already has data and,
    # if so, find out where we left off
    if os.path.exists(save_location):
        existing_df = pd.read_csv(save_location)
        start_game = len(existing_df)
    else:
        start_game = 0

    # Load PGN
    pgn = open(pgn_file)

    # Estimate total games in the PGN file
    total_games = count_games_in_pgn(pgn_file)

    # Skip games that are already processed (based on existing data in the CSV)
    for _ in range(start_game):
        _ = read_game(pgn)

    # Define the generator for games
    game_generator = iter(lambda: read_game(pgn), None)

    # Calculate the total number of games remaining to process
    remaining_games = total_games - start_game

    # Set up the tqdm progress bar
    progress_bar = tqdm(game_generator, total=remaining_games, desc="Processing games")

    # Process games
    for game_idx, game in enumerate(progress_bar, start=start_game):
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

        # Save to CSV every N games or if it's the last game
        if (game_idx + 1) % save_interval == 0 or game_idx == total_games - 1:
            temp_df = pd.DataFrame(games)
            if os.path.exists(save_location):
                temp_df.to_csv(save_location, mode="a", header=False, index=False)
            else:
                temp_df.to_csv(save_location, mode="w", header=True, index=False)

            # Clear the games list to free up memory
            games.clear()

    return pd.read_csv(save_location)  # Return the final dataframe
