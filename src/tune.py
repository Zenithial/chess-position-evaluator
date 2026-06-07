from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV

def parameter_tuning(X_train, y_train, X_test, y_test):
    param_grid = {
        "n_estimators": [100, 300],
        "max_features": ["sqrt", 1/3, 0.5],
        "max_depth": [None, 10, 20]
    }
    grid = GridSearchCV(
        RandomForestRegressor(random_state=42),
        param_grid,
        cv=5,
        scoring="r2",
        n_jobs=2
    )
    grid.fit(X_train, y_train)
    
    print("Best params:", grid.best_params_)
    print("Best CV R2:", grid.best_score_)
    print("Test R2:", grid.best_estimator_.score(X_test, y_test))