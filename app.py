# Import libraries
import requests
import pandas as pd
import numpy as np
from flask import Flask, request, jsonify
import json
import pickle
import joblib

subject_id = 1.

app = Flask(__name__)


def _load_test_data():
    """

    :return:
    """
    df = pickle.load(
        open("test_data_sub" + str(subject_id) + ".p", "rb"))
    return df[np.random.choice(len(df), 1)[0], :].tolist()


app = Flask(__name__)

# Load the model
model = joblib.load('model_sub' + str(subject_id) + '.pkl')


@app.route('/api', methods=['GET'])
def predict():
    # Get the data from the POST request.
    # data = request.get_json(force=True)
    data = _load_test_data()

    # Make prediction using model loaded from disk as per the data.
    prediction = model.predict([np.array(data)])

    # Take the first value of prediction
    output = prediction[0]

    return json.dumps({"success": True, "data": output})


if __name__ == '__main__':
    try:
        app.run(port=5000, host='0.0.0.0', debug=True)
    except:
        print("Server is exited unexpectedly. Please contact server admin.")
