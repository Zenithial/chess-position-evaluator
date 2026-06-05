import chess
from src.process_data import count_material
from src.process_data import space_diff
from src.process_data import has_bishop_pair
from src.process_data import can_castle
from src.process_data import development_diff
from src.process_data import count_legal_moves
from src.process_data import in_check
from src.process_data import white_to_move
from src.process_data import count_doubled_pawns
from src.process_data import preprocess_position_string
from src.process_data import count_pawn_islands
from src.process_data import count_passed_pawns
from src.process_data import passed_pawn_diff

def test_count_material():
    example_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1" # The start position
    material_diff = count_material(example_fen)
    assert material_diff == 0
    
def test_space_diff():
    example_fen = "rnbqkbnr/pp3ppp/2ppp3/8/2PPP3/8/PP3PPP/RNBQKBNR w KQkq - 0 4"
    space_difference = space_diff(example_fen)
    assert space_difference == 3
    
def test_has_bishop_pair():
    example_fen = "rnb1kb1r/pppp1pp1/4pq1p/8/3PP3/8/PPP2PPP/RN1QKBNR w KQkq - 0 5"
    bishop_pair_difference = has_bishop_pair(example_fen)
    assert bishop_pair_difference == -1
    
def test_count_castling_rights():
    example_fen = "rnbqkbnr/pppp1ppp/8/4p3/4P3/8/PPPPKPPP/RNBQ1BNR b kq - 1 2"
    count_castling_rights_difference = can_castle(example_fen)
    assert count_castling_rights_difference == -2
    example_fen_two = "8/8/8/4p1K1/2k1P3/8/8/8 b - - 0 1"
    count_castling_rights_difference_two = can_castle(example_fen_two)
    assert count_castling_rights_difference_two == 0
    
def test_back_rank_diff():
    example_fen = "rnbqkb1r/pppppppp/5n2/8/2PP1B2/2NBPN2/PP3PPP/R2QK2R w KQkq - 3 8"
    count_back_rank_diff = development_diff(example_fen)
    assert count_back_rank_diff == 3
    
def test_legal_moves():
    example_fen = "8/Bp6/1P6/8/6p1/5p1p/4kPPP/6KR w - - 0 1"
    count_all_legal_moves = count_legal_moves(example_fen)
    assert count_all_legal_moves == 4
    
def test_in_check():
    example_fen = "rnbqkbnr/pp2pppp/3p4/1Bp5/4P3/5N2/PPPP1PPP/RNBQK2R b KQkq - 1 3"
    is_in_check = in_check(example_fen)
    assert is_in_check == True
    
def test_white_to_move():
    example_fen = "rn1qkbnr/pp1bpppp/3p4/1Bp5/4P3/5N2/PPPP1PPP/RNBQK2R w KQkq - 2 4"
    is_white_to_move = white_to_move(example_fen)
    assert is_white_to_move == True
    
def test_position_string_preprocessing():
    string = "2P4p"
    new_string = preprocess_position_string(string)
    assert new_string == "EEPEEEEp"
    
def test_doubled_pawns_diff():
    example_fen = "r1bqk2r/pp1pppb1/2P2n1p/2P5/2P4p/8/P3PPP1/RNBQKBNR w KQkq - 0 8"
    doubled_pawns_diff = count_doubled_pawns(example_fen)
    assert doubled_pawns_diff == -1
    
def test_count_isolated_pawns():
    example_fen = "rnbqkbnr/1ppp1pp1/8/P3p2P/8/8/P1PPPP1P/RNBQKBNR b KQkq - 0 4"
    pawn_island_diff = count_pawn_islands(example_fen)
    assert pawn_island_diff == -2
    
def test_number_of_white_passed_pawns():
    example_fen = "r1b1k1nr/4ppbP/P5p1/1PP5/2p5/2N5/3PPP2/R1BQK1NR w KQkq - 0 1"
    white_passed_pawns = count_passed_pawns(example_fen, chess.WHITE, chess.BLACK)
    assert white_passed_pawns == 4
    
def test_number_of_black_passed_pawns():
    example_fen = "k6B/1p5N/3p4/P3p3/p1p1p1p1/6P1/3P2K1/8 w - - 0 1"
    black_passed_pawns = count_passed_pawns(example_fen, chess.BLACK, chess.WHITE)
    assert black_passed_pawns == 1

def test_count_passed_pawns_diff():
    example_fen = "r1b1k1nr/p3ppbp/6p1/2P5/2p5/2N5/3PPP2/R1BQK1NR w KQkq - 0 1"
    passed_pawn_difference = passed_pawn_diff(example_fen)
    assert passed_pawn_difference == -1