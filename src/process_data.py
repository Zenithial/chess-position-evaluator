import pandas as pd
import chess
from sklearn.model_selection import train_test_split

# df = pd.read_csv('data/train.csv')

# str_df = df.to_string()

feature_map = {"material_diff": 0, 
               "space_diff": 0, 
               "bishop_pair_diff": 0, 
               "king_safety_diff": 0, 
               "development_diff": 0,
               "legal_moves": 0,
               "in_check": 0,
               "white_to_move": 0,
               "pawn_islands_diff": 0,
               "doubled_pawns_diff": 0,
               "passed_pawns_diff": 0
               }

piece_values = {"p": 100,
                "P": 100,
                "n": 300,
                "N": 300,
                "b": 325,
                "B": 325,
                "r": 500,
                "R": 500,
                "q": 900,
                "Q": 900}

def count_material(position):
    white_material_count = 0
    black_material_count = 0
    for i in range(len(position)):
        piece = position[i]
        if piece in piece_values:
            if piece.islower():
                black_material_count += piece_values.get(piece)
            else:
                white_material_count += piece_values.get(piece)
    return white_material_count - black_material_count

def space_diff(position):
    white_piece_count = 0
    black_piece_count = 0
    fields = position.split("/")
    fourth_and_fifth_rank = fields[3] + fields[4]
    for i in range(len(fourth_and_fifth_rank)):
        if fourth_and_fifth_rank[i].isalpha():
            if fourth_and_fifth_rank[i].islower():
                black_piece_count += 1
            else:
                white_piece_count += 1
    return white_piece_count - black_piece_count

def has_bishop_pair(position):
    white_has_bishop_pair = 0
    black_has_bishop_pair = 0
    white_bishop_count = 0
    black_bishop_count = 0
    for i in range(len(position)):
        if position[i] == "B":
            white_bishop_count += 1
        if position[i] == "b":
            black_bishop_count += 1
    if white_bishop_count == 2:
        white_has_bishop_pair = 1
    if black_bishop_count == 2:
        black_has_bishop_pair = 1
    return white_has_bishop_pair - black_has_bishop_pair

def can_castle(position):
    white_castling_options = 0
    black_castling_options = 0
    fields = position.split()
    for i in range(len(fields[2])):
        match fields[2][i]:
            case "-":
                return 0
            case "K":
                white_castling_options += 1
            case "Q":
                white_castling_options += 1
            case "k":
                black_castling_options += 1
            case "q":
                black_castling_options += 1
    
    return white_castling_options - black_castling_options

def development_diff(position):
    white_back_rank_count = 0
    black_back_rank_count = 0
    fields = position.split("/")
    back_ranks = fields[0] + fields[-1]
    for i in range(len(back_ranks)):
        if back_ranks[i].islower():
            black_back_rank_count += 1
        elif back_ranks[i].isupper():
            white_back_rank_count += 1
        elif back_ranks[i] == " ":
            break
    
    return white_back_rank_count - black_back_rank_count

def count_legal_moves(position):
    board = chess.Board(position)
    return board.legal_moves.count()

def in_check(position):
    board = chess.Board(position)
    return board.is_check()

def white_to_move(position):
    return "w" in position
        
# print(df)
