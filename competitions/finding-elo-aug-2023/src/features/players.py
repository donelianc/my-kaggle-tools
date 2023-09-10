# Functions to extract key data from each game
def get_player_ratings(game):
    """Get player Elo ratings from PGN headers"""
    white_rating = game.headers["WhiteElo"]
    black_rating = game.headers["BlackElo"]

    return {"wp_rating": white_rating, "bp_rating": black_rating}
