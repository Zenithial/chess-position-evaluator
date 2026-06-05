import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from process_data import (
    count_material,
    space_diff,
    has_bishop_pair,
    can_castle,
    development_diff,
    count_legal_moves,
    in_check,
    white_to_move,
    count_doubled_pawns,
    count_pawn_islands,
    passed_pawn_diff
)

def apply_features(row):
    board = row["FEN"]
    return {
        "material_diff": count_material(board), 
        "space_diff": space_diff(board), 
        "bishop_pair_diff": has_bishop_pair(board), 
        "king_safety_diff": can_castle(board), 
        "development_diff": development_diff(board),
        "legal_moves": count_legal_moves(board),
        "in_check": in_check(board),
        "white_to_move": white_to_move(board),
        "pawn_islands_diff": count_pawn_islands(board),
        "doubled_pawns_diff": count_doubled_pawns(board),
        "passed_pawns_diff": passed_pawn_diff(board)
    }

df = pd.read_csv('data/train.csv')
df_small = df.sample(n=100000, random_state=42)
features = df_small.apply(apply_features, axis=1, result_type="expand")

X_train, X_test, y_train, y_test = train_test_split(features, df_small["Evaluation"], random_state=42)

forest = RandomForestRegressor(n_estimators=300, random_state=42)
forest.fit(X_train, y_train)
print(forest.score(X_test, y_test))
print(pd.Series(forest.feature_importances_, index=X_train.columns).sort_values(ascending=False))