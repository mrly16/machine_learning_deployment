import os

import numpy as np
import pandas as pd
import joblib
from sklearn.preprocessing import OneHotEncoder

from constant import ENCODER_PATH, ENCODING_COL_LIST
from src.util.path_util import get_project_root


def build_features(df, is_trained=False):
    df['completion_year'] = df['completion_year'].apply(lambda x: float(str(x)[:4]) if x else np.nan)
    df['community_age'] = (2021 - df['completion_year'].astype(float)).astype(float)
    df['real_estate_type'] = df['real_estate_type'].astype(float)
    if is_trained:
        df_processed = _encode_test_data(df)
        return df_processed.fillna(0)
    else:
        df_processed = _train_onehot_encoder(df)
        return df_processed.fillna(0)


def _train_onehot_encoder(df):
    enc = OneHotEncoder(handle_unknown='ignore', sparse=False)
    df_enc, enc = _onehot_encoding(df, enc, ENCODING_COL_LIST)
    joblib.dump(enc, os.path.join(get_project_root(), ENCODER_PATH))
    return df_enc


def _encode_test_data(test_df):
    enc = joblib.load(os.path.join(get_project_root(), ENCODER_PATH))
    test_df_enc, _ = _onehot_encoding(test_df, enc, ENCODING_COL_LIST, False)
    return test_df_enc


def _onehot_encoding(df, encoder, col_list, for_training=True):
    original_df = df.drop(col_list, axis=1).reset_index(drop=True)
    df[col_list] = df[col_list].fillna('missing')
    if for_training:
        df_dummy = encoder.fit_transform(df[col_list])
        encoded_df = pd.DataFrame(df_dummy, columns=encoder.get_feature_names()).reset_index(
            drop=True)
    else:
        encoded_df = pd.DataFrame(encoder.transform(df[col_list]), columns=encoder.get_feature_names()).reset_index(
            drop=True)
    df_enc = pd.concat([original_df, encoded_df], axis=1)
    return df_enc, encoder
