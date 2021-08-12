import numpy as np
import pandas as pd

from constant import OUTLIER_FACTOR, SIMPLE_MODEL_FEATURE_LIST
from src.features.build_features import build_features
from src.util.postgres_util import get_conn
from src.util.sql_util import LOAD_RAW_DATA


class CommunityDataset:
    def __init__(self,
                 sample_size=50000,
                 kept_cols=SIMPLE_MODEL_FEATURE_LIST,
                 is_trained=False,
                 input_df=None):
        self.sample_size = sample_size
        self.kept_cols = kept_cols
        self.is_trained = is_trained
        if input_df:
            self.df = input_df
        else:
            self.df = self.load_data()

        self.process_data()

    def load_data(self):
        # Loading data from data warehouse
        with get_conn() as conn:
            df = pd.read_sql(LOAD_RAW_DATA.format(sample_size=self.sample_size), conn)
        return df[self.kept_cols]

        # num_cols = [col for col in df.dtypes[df.dtypes != object].index if col != 'price']
        # obj_cols = [col for col in df.dtypes[df.dtypes == object].index.tolist() if col != 'tags']
        # target_col = 'price'
        # return df[num_cols + obj_cols + [target_col]], num_cols, obj_cols, target_col

    @staticmethod
    def _convert_datatype(df):
        # Converting data types and taking care of null values
        df = df.replace('', np.nan)
        return df

    # def _drop_high_missing(self, df):
    #     # Excluding rows with very high missing value rate
    #     df = df[df.columns[df.notnull().mean() > self.thres_row]]
    #
    #     # Excluding columns with very high missing value rate
    #     df = df.loc[df.notnull().mean(axis=1) > self.thres_col]
    #
    #     self.kept_cols = df.columns
    #     return df

    def _feature_imputation(self, df):
        # Imputing numerical features with 0
        num_cols = [col for col in df.dtypes[df.dtypes != object].index if col != 'price']
        df[num_cols] = df[num_cols].fillna(0)

        # categorical_imputation
        if self.is_trained:
            df['building_type'].fillna('多层', inplace=True)
        else:
            df['building_type'].fillna(df['building_type'].value_counts().idxmax(), inplace=True)
        return df

    @staticmethod
    def _drop_outliers(df):
        # Dropping the outlier rows with standard deviation
        upper_lim = df['total_household_num'].mean() + df['total_household_num'].std() * OUTLIER_FACTOR
        lower_lim = df['total_household_num'].mean() - df['total_household_num'].std() * OUTLIER_FACTOR

        df = df[(df['total_household_num'] < upper_lim) & (df['total_household_num'] > lower_lim)]
        return df

    def process_data(self):
        df = self._convert_datatype(self.df)
        df = self._feature_imputation(df)
        if not self.is_trained:
            df = self._drop_outliers(df)
        self.df = build_features(df, self.is_trained)
