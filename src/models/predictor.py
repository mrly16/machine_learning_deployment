import os

import joblib
import pandas as pd
from sklearn.base import BaseEstimator
from sklearn.ensemble import ExtraTreesRegressor
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_validate
from xgboost import XGBRegressor

from constant import ID_COLUMN, TARGET_COL, RANDOM_SEED
from src.util.log_util import logger
from src.util.path_util import get_project_root


class Predictor(BaseEstimator):
    def __init__(self,
                 verbose=True,
                 feature_dict={},
                 algorithm='etr',
                 algorithm_params=None,
                 keep_data=True,
                 drop_tails=True,
                 only_common_columns=True):
        self.drop_tails = drop_tails
        self.keep_data = keep_data
        self.feature_dict = feature_dict
        self.only_common_columns = only_common_columns
        self.algorithm = algorithm
        self.algorithm_params = algorithm_params
        self.verbose = verbose

        if self.algorithm == 'etr':
            self.model = ExtraTreesRegressor(**self.algorithm_params)
        elif self.algorithm == 'xgb':
            self.model = XGBRegressor(**self.algorithm_params)
        else:
            self.model = LogisticRegression(**self.algorithm_params)

    def fit(self, X, y):
        self.model.fit(X, y)

    def train(self, X, y):
        return self.model.fit(X, y)

    def predict(self, X):
        return self.model.predict(X)

    def predict_with_X(self, X):
        new_X = X.copy()
        new_X[TARGET_COL] = self.model.predict(X)
        return new_X


class StackedPredictor(Predictor):
    def __init__(self, params_for_predictor_dict,
                 verbose=True,
                 feature_dict={},
                 src_path=None,
                 input_df=None,
                 algorithm=None,
                 algorithm_params=None,
                 keep_data=True,
                 drop_tails=True,
                 only_common_columns=True,
                 random_state=RANDOM_SEED,
                 kfolds=3):
        self.predictors = []
        self.params_for_predictor_dict = params_for_predictor_dict
        self.verbose = verbose
        self.drop_tails = drop_tails
        self.keep_data = keep_data
        self.feature_dict = feature_dict
        self.only_common_columns = only_common_columns
        self.algorithm_params = algorithm_params
        self.random_state = random_state
        self.kfolds = kfolds
        self.root = str(get_project_root())

        super(StackedPredictor, self).__init__(verbose=verbose,
                                               feature_dict=feature_dict,
                                               algorithm=algorithm,
                                               algorithm_params=algorithm_params,
                                               keep_data=keep_data,
                                               drop_tails=drop_tails,
                                               only_common_columns=only_common_columns)
        if input_df is not None:
            self.data = input_df
        else:
            self.data = pd.read_csv(src_path)
        self.X = self.data[[col for col in self.data.columns if col != TARGET_COL]]
        self.y = self.data[TARGET_COL]
        del self.data

        logger.info('Training kfolds of low-level Models...')
        for params in self.params_for_predictor_dict:
            self.predictors.append(
                cross_validate(Predictor(**params), self.X, self.y, cv=self.kfolds, verbose=self.verbose,
                               scoring='neg_mean_absolute_error', return_estimator=True)['estimator'])

        stacked_X = self.kfold_predictor_predictions()
        logger.info('Training Stacked Model...')
        self.model = super(StackedPredictor, self).train(stacked_X, self.y)
        joblib.dump(self.model, os.path.join(self.root, f'models/model.pkl'))

        if keep_data:
            self.data = stacked_X

    def kfold_predictor_predictions(self):
        stacked_data = self.X.copy()

        # Generate the predictions for each predictors
        for i, pred_cv in enumerate(self.predictors):
            for j, pred in enumerate(pred_cv):
                joblib.dump(pred, os.path.join(self.root, f'models/submodel_{i}_{j}.pkl'))
                aux = pred.predict_with_X(self.X)
                aux.rename(columns={TARGET_COL: 'pred_' + str(i + 1) + str(j + 1)}, inplace=True)
                stacked_data = stacked_data.merge(aux[[ID_COLUMN, 'pred_' + str(i + 1) + str(j + 1)]], on=ID_COLUMN,
                                                  how='left')

        return stacked_data
