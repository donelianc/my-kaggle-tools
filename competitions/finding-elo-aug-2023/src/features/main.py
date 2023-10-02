import gc
import os
from typing import Dict, List, Optional, Union

import pandas as pd
from chess.pgn import Game, read_game
from src.features.game import (
    get_captures,
    get_castling,
    get_checks,
    get_game_info,
    get_piece_moves,
    get_promotions,
)
from src.features.opening import get_opening_features
from src.features.players import get_player_ratings
from src.features.utils import count_games_in_pgn
from tqdm import tqdm


def pgn_to_dataframe(
    pgn_file: str,
    include_opening_cols: bool = True,
    save_to_file: bool = True,
    save_interval: int = 100,
    save_location: str = "./data/interim/output.csv",
) -> Optional[pd.DataFrame]:
    """
    Converts a PGN file to a Pandas DataFrame with
    an option to save intermittently to CSV.

    Parameters:
    pgn_file (str):
        The file path of the PGN file to be converted.
    save_interval (int):
        The number of games processed before saving to CSV. Default is 100.
    save_location (str):
        The location to save the DataFrame as CSV. Default is "./../../output.csv".
    include_opening_cols (bool):
        Flag to determine whether to include opening features. Default is True.
    save_to_file (bool):
        Flag to control whether to write the DataFrame to a CSV file. Default is True.

    Returns:
    Optional[pd.DataFrame]: The resulting DataFrame if successful, None otherwise.
    """

    games = []
    start_game = 0

    # Check if save_location already has data and find out where we left off.
    if os.path.exists(save_location):
        try:
            existing_df = pd.read_csv(save_location)
            start_game = len(existing_df)
        except Exception as e:
            print(f"Error reading existing DataFrame: {e}")

    try:
        with open(pgn_file) as pgn:
            total_games = count_games_in_pgn(pgn_file)
            remaining_games = total_games - start_game
            progress_bar = tqdm(
                iter(lambda: read_game(pgn), None),
                total=remaining_games,
                desc="Processing games",
            )

            for game_idx, game in enumerate(progress_bar, start=start_game):
                game_data = extract_game_data(game, include_opening_cols)
                games.append(game_data)

                if save_to_file and (
                    (game_idx + 1) % save_interval == 0 or game_idx == total_games - 1
                ):
                    save_games_to_csv(games, save_location)
                    games.clear()
                    gc.collect()

            final_df = (
                pd.DataFrame(games) if not save_to_file else pd.read_csv(save_location)
            )
            return final_df

    except Exception as e:
        print(f"Error processing PGN file: {e}")
        return None


def extract_game_data(
    game: Game, include_opening_cols: bool
) -> Dict[str, Union[str, int, float]]:
    """
    Extracts relevant information from a chess game.

    Parameters:
    game (Game):
        A chess game object.
    include_opening_cols (bool):
        Flag to determine whether to include opening features.

    Returns:
    Dict[str, Union[str, int, float]]: A dictionary containing extracted game data.
    """

    player_ratings = get_player_ratings(game)
    game_info = get_game_info(game)
    piece_moves = get_piece_moves(game)
    check_counts = get_checks(game)
    capture_counts = get_captures(game)
    promotion_counts = get_promotions(game)
    castling_counts = get_castling(game)

    game_data = {
        **player_ratings,
        **game_info,
        **piece_moves,
        **check_counts,
        **capture_counts,
        **promotion_counts,
        **castling_counts,
    }

    if include_opening_cols:
        opening_features = get_opening_features(game)
        game_data = {**game_data, **opening_features}

    return game_data


def save_games_to_csv(
    games: List[Dict[str, Union[str, int, float]]], save_location: str
) -> None:
    """
    Saves a list of games to a CSV file.

    Parameters:
    games (List[Dict[str, Union[str, int, float]]]):
        A list of games represented as dic.
    save_location (str):
        The location to save the CSV file.
    """

    temp_df = pd.DataFrame(games)
    mode = "a" if os.path.exists(save_location) else "w"
    header = not os.path.exists(save_location)

    try:
        temp_df.to_csv(save_location, mode=mode, header=header, index=False)
    except Exception as e:
        print(f"Error writing to CSV: {e}")
