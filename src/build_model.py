import chess
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from tune import parameter_tuning
from process_data import (
    count_material,
    space_diff,
    has_bishop_pair,
    can_castle,
    development_diff,
    count_doubled_pawns,
    count_pawn_islands,
    passed_pawn_diff,
    isolated_pawn_diff
)

def apply_features(row):
    fen = row["FEN"]
    board = chess.Board(fen)
    return {
        "material_diff": count_material(fen), 
        "space_diff": space_diff(fen), 
        "bishop_pair_diff": has_bishop_pair(fen), 
        "king_safety_diff": can_castle(fen),
        "development_diff": development_diff(fen),
        "legal_moves": board.legal_moves.count(),
        "in_check": int(board.is_check()),
        "white_to_move": int(board.turn == chess.WHITE),
        "pawn_islands_diff": count_pawn_islands(fen),
        "doubled_pawns_diff": count_doubled_pawns(fen),
        "passed_pawns_diff": passed_pawn_diff(board),
        "isolated_pawns_diff": isolated_pawn_diff(board)
    }

df = pd.read_csv('data/train.csv')
df_small = df.sample(n=100000, random_state=42)
features = df_small.apply(apply_features, axis=1, result_type="expand")

X_train, X_test, y_train, y_test = train_test_split(features, df_small["Evaluation"], random_state=42)

# parameter_tuning(X_train, y_train, X_test, y_test)

#default_forest = RandomForestRegressor(n_jobs=2, random_state=42)
#default_forest.fit(X_train, y_train)
#print(default_forest.score(X_test, y_test))
#print(pd.Series(default_forest.feature_importances_, index=X_train.columns).sort_values(ascending=False))
tuned_forest = RandomForestRegressor(n_estimators=300, max_depth=20, max_features="sqrt", n_jobs=2, random_state=42)
tuned_forest.fit(X_train, y_train)
print(tuned_forest.score(X_test, y_test))
print(pd.Series(tuned_forest.feature_importances_, index=X_train.columns).sort_values(ascending=False))