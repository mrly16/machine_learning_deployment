CONFIG_PATH = 'config.ini'

OUTLIER_FACTOR = 3
RANDOM_SEED = 42
SIMPLE_MODEL_FEATURE_LIST = ['community_id', 'city_id', 'district_id', 'area_id', 'total_area', 'plot_ratio', 'landscaping_ratio', 'total_household_num', 'photo_num', 'video_num', 'sale_num', 'rent_num', 'overall_score', 'shopping_score', 'traffic_score', 'impression_score', 'building_type', 'real_estate_type', 'completion_year', 'community_type', 'market_sentiment', 'price']
ID_COLUMN = 'community_id'
TARGET_COL = 'price'

ENCODER_PATH = 'models/onehot_encoder.pkl'
ENCODING_COL_LIST = ["building_type", "market_sentiment", "community_type"]

PARAM_XGB_1 = {'algorithm': 'xgb',
               'algorithm_params': {'learning_rate': 0.02,
                                    'n_estimators': 200,
                                    'max_depth': 4,
                                    'min_child_weight': 2,
                                    'gamma': 0.9,
                                    'subsample': 0.8,
                                    'colsample_bytree': 0.8,
                                    'objective': 'reg:squarederror'}}

PARAM_XGB_2 = {'algorithm': 'xgb',
               'algorithm_params': {'learning_rate': 0.05,
                                    'n_estimators': 20,
                                    'max_depth': 6,
                                    'min_child_weight': 2,
                                    'gamma': 0.9,
                                    'subsample': 0.8,
                                    'colsample_bytree': 0.8,
                                    'objective': 'reg:squarederror'}}

PARAM_XGB_3 = {'algorithm': 'xgb',
               'algorithm_params': {'learning_rate': 0.01,
                                    'n_estimators': 50,
                                    'max_depth': 9,
                                    'min_child_weight': 2,
                                    'gamma': 0.9,
                                    'subsample': 0.8,
                                    'colsample_bytree': 0.8,
                                    'objective': 'reg:squarederror'}}
