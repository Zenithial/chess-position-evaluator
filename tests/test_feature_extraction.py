from src.process_data import count_material
from src.process_data import space_diff
from src.process_data import has_bishop_pair
from src.process_data import can_castle
from src.process_data import development_diff
from src.process_data import count_legal_moves
from src.process_data import in_check
from src.process_data import white_to_move

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
    assert count_back_rank_diff == -3
    
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
    