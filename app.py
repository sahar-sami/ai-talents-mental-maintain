# Import libraries
import requests
import pandas as pd
import numpy as np
import datetime
from flask import Flask, request, jsonify
import json
import pickle
import joblib
import os

subject_id = 1.
display_dict = {}

app = Flask(__name__)


def _load_test_data():
    """

    :return:
    """
    df = pickle.load(open("data" + os.sep + "test_data_sub" + str(subject_id) + ".p", "rb"))
    _idx = np.random.choice(len(df), 1)[0]
    display_dict['Heart Rate'] = df[_idx, 6]
    display_dict['pNN25'] = df[_idx, 7]
    display_dict['pNN50'] = df[_idx, 8]
    return df[_idx, :].tolist()


app = Flask(__name__)

# Load the model
model = joblib.load('models' + os.sep + 'model_sub' + str(subject_id) + '.pkl')


@app.route('/api', methods=['GET'])
def predict():
    # Get the data from the POST request.
    # data = request.get_json(force=True)
    data = _load_test_data()

    # Make prediction using model loaded from disk as per the data.
    prediction = model.predict([np.array(data)])

    # Take the first value of prediction
    output = prediction[0]

    now = datetime.datetime.now()

    display_dict.update({"success": True, "data": output, "Current date and time": now.strftime("%Y-%m-%d %H:%M:%S")})
    return json.dumps(display_dict)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=int(os.environ.get("PORT", 8080)))
