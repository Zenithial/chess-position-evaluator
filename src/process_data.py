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
    
    return black_back_rank_count - white_back_rank_count

def count_legal_moves(position):
    board = chess.Board(position)
    return board.legal_moves.count()

def in_check(position):
    board = chess.Board(position)
    return board.is_check()

def white_to_move(position):
    return "w" in position

def count_doubled_pawns(position):
    white_doubled_pawns = 0
    black_doubled_pawns = 0
    expanded_position = preprocess_position_string(position)
    fields = expanded_position.split("/")
    count_white_pawns = 0
    count_black_pawns = 0
    for i in range(len(fields)):
        for j in range(len(fields[0])):
            if fields[j][i] == "p":
                count_black_pawns += 1
            elif fields[j][i] == "P":
                count_white_pawns += 1
        if (count_black_pawns >= 2):
            black_doubled_pawns += count_black_pawns - 1
        if (count_white_pawns >= 2):
            white_doubled_pawns += count_white_pawns - 1
        count_white_pawns = 0
        count_black_pawns = 0
    
    return black_doubled_pawns - white_doubled_pawns

def count_pawn_islands(position):
    black_pawn_island_count = 0
    white_pawn_island_count = 0
    no_pawn_columns = find_no_pawn_columns(position)
    black_pawn_island_count = update_pawn_island_count(no_pawn_columns[0], black_pawn_island_count)
    white_pawn_island_count = update_pawn_island_count(no_pawn_columns[1], white_pawn_island_count)
    return black_pawn_island_count - white_pawn_island_count

def passed_pawn_diff(position):
    white_passed_pawn_count = count_passed_pawns(position, chess.WHITE, chess.BLACK)
    black_passed_pawn_count = count_passed_pawns(position, chess.BLACK, chess.WHITE)
    return white_passed_pawn_count - black_passed_pawn_count

def count_passed_pawns(position, colour, opposing_colour):
    board = chess.Board(position)
    passed_pawn_count = 0
    is_passed = True
    for pawn in board.pieces(chess.PAWN, colour):
        file = chess.square_file(pawn)  
        rank = chess.square_rank(pawn)
        for opposite_colour_pawn in board.pieces(chess.PAWN, opposing_colour):
            file_two = chess.square_file(opposite_colour_pawn)
            rank_two = chess.square_rank(opposite_colour_pawn)
            if colour == chess.WHITE:
                if abs(file - file_two) <= 1 and rank_two > rank:
                    is_passed = False
                    break
            elif colour == chess.BLACK:
                if abs(file - file_two) <= 1 and rank_two < rank:
                    is_passed = False
        if is_passed:
             passed_pawn_count += 1
        else:
            is_passed = True
    return passed_pawn_count

def find_no_pawn_columns(position):
    black_contains_pawn = [False, False, False, False, False, False, False, False]
    white_contains_pawn = [False, False, False, False, False, False, False, False]
    expanded_position = preprocess_position_string(position)
    fields = expanded_position.split("/")
    for i in range(len(fields)):
        for j in range(len(fields[0])):
            if fields[j][i] == "p":
                black_contains_pawn[i] = True
            elif fields[j][i] == "P":
                white_contains_pawn[i] = True
    return (black_contains_pawn, white_contains_pawn)

def update_pawn_island_count(column_contains_pawn, pawn_island_count): 
    encountered_pawn = False
    for i in range(len(column_contains_pawn)):
        if column_contains_pawn[i] == True:
            if encountered_pawn == False:
                pawn_island_count += 1
            encountered_pawn = True
        else:
            encountered_pawn = False
    return pawn_island_count
    
def preprocess_position_string(position):
    board = position.split()[0]
    expanded = ""
    for i in range(len(board)):
        if board[i].isdigit():
            num = int(board[i])
            expanded += "E" * num
        else:
            expanded += board[i]
            
    return expanded
        
# print(df)
