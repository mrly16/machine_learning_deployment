import os

import joblib
from flask import Flask, Response

from constant import PARAM_XGB_1, PARAM_XGB_2, PARAM_XGB_3, ID_COLUMN, TARGET_COL
from src.data.make_dataset import CommunityDataset
from src.data.stacked_transform import stacked_transform
from src.models.predictor import StackedPredictor

from src.util.path_util import get_project_root

STACKED_MODEL_PATH = os.path.join(get_project_root(), 'models/model.pkl')

app = Flask(__name__)


@app.route('/train')
def train():
    community_dataset = CommunityDataset(sample_size=1000)
    StackedPredictor(params_for_predictor_dict=[PARAM_XGB_1, PARAM_XGB_2],
                     input_df=community_dataset.df,
                     **PARAM_XGB_3)
    return 'Model trained'


@app.route('/inference')
def inference():
    community_dataset = CommunityDataset(sample_size=100, is_trained=True)
    df_result = stacked_transform(community_dataset.df, 3)
    stacked_model = joblib.load(STACKED_MODEL_PATH)
    df_result[TARGET_COL] = stacked_model.predict(df_result)
    return Response(df_result[[ID_COLUMN, TARGET_COL]].to_json(orient="records"), mimetype='application/json')


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
