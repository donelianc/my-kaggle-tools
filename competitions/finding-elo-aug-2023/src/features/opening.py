from time import sleep

import chess
import requests

# Define the base URL as a constant
BASE_URL = "https://explorer.lichess.ovh/{database}"


def get_opening_name(fen, database="lichess", until="2012", sleep_time=5):
    """
    Fetch the opening name based on FEN notation from Lichess API.

    :param fen: The FEN notation string.
    :param database: The database to query, default is 'lichess'.
    :param until: The cut-off year for data, default is '2012'.
    :param sleep_time: Duration before making a request, default is 5 seconds.
    :return: tuple containing the opening name and the full data.
    """
    sleep(sleep_time)
    url = BASE_URL.format(database=database)
    response = requests.get(f"{url}?fen={fen}&until={until}")

    # Ensure the response is valid
    response.raise_for_status()

    # Parse the JSON response
    try:
        data = response.json()
        # Ensure the data is a dictionary
        if not isinstance(data, dict):
            raise ValueError("Unexpected response format from API")
    except ValueError as e:
        print(f"Error parsing JSON: {e}")
        data = {}

    # Extract the opening name
    name = None
    if "opening" in data.keys():
        if data["opening"] is not None:
            name = data["opening"].get("name")

    return name, data


def get_opening_features(game):
    """
    Get opening features from a game.
    """
    board = game.board()
    main_moves = list(game.mainline_moves())
    total_moves = len(main_moves)

    # Initial states
    (
        opening_name,
        opening_last_move,
        opening_last_known_move,
        opening_moves_after_novelty,
        opening_novelty_player,
        opening_novelty_piece,
        opening_novelty_square,
        opening_novelty_move,
    ) = (None, None, None, None, None, None, None, None)

    for i, move in enumerate(main_moves):
        fen = board.fen()
        opening, data = (
            (None, {"moves": [None]})
            if i == 0
            else get_opening_name(fen=fen, database="master", sleep_time=2)
        )

        if opening:
            opening_name = opening
            opening_last_move = i

        # If no moves in data or we're at the last move
        if not data["moves"]:
            break
        elif i == total_moves - 1:
            opening_moves_after_novelty = 0
            (
                opening_novelty_player,
                opening_novelty_piece,
                opening_novelty_square,
                opening_novelty_move,
            ) = (None, None, None, None)
            break

        opening_last_known_move = i

        opening_novelty_piece = board.piece_at(move.from_square)
        opening_novelty_piece = opening_novelty_piece.symbol().upper()

        opening_novelty_square = chess.square_name(move.to_square)
        opening_novelty_move = board.san(move)
        opening_novelty_player = fen.split(" ")[1] + "p"

        opening_moves_after_novelty = total_moves - opening_last_known_move

        board.push(move)

    return {
        "opening_name": opening_name,
        "opening_last_move": opening_last_move,
        "opening_last_known_move": opening_last_known_move,
        "opening_moves_after_novelty": opening_moves_after_novelty,
        "opening_novelty_player": opening_novelty_player,
        "opening_novelty_piece": opening_novelty_piece,
        "opening_novelty_square": opening_novelty_square,
        "opening_novelty_move": opening_novelty_move,
    }
