def count_games_in_pgn(pgn_file):
    with open(pgn_file, "r") as file:
        content = file.readlines()
    return sum(1 for line in content if line.startswith("[Event "))
