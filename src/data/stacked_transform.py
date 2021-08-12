import os

import joblib

from constant import TARGET_COL, ID_COLUMN
from src.util.path_util import get_project_root


def stacked_transform(df, n_models):
    X = df[[col for col in df.columns if col != TARGET_COL]]
    stacked_data = X.copy()
    for i in range(2):
        for j in range(n_models):
            filename = os.path.join(get_project_root(), f'models/submodel_{i}_{j}.pkl')
            model = joblib.load(filename)
            aux = model.predict_with_X(X)
            aux.rename(columns={TARGET_COL: 'pred_' + str(i + 1) + str(j + 1)}, inplace=True)
            stacked_data = stacked_data.merge(aux[[ID_COLUMN, 'pred_' + str(i + 1) + str(j + 1)]], on=ID_COLUMN,
                                              how='left')
    return stacked_data
