from flask import Flask, jsonify, request
from flask_cors import CORS
import pymongo
import requests
import pandas as pd
import numpy as np
import datetime
import json
import pickle
import joblib
import os

subject_id = 1.
display_dict = {}


def _load_test_data():
    """
    :return:
    """
    df = pickle.load(open("data" + os.sep + "test_data_sub" +
                          str(subject_id) + ".p", "rb"))
    _idx = np.random.choice(len(df), 1)[0]
    display_dict['heart_rate'] = df[_idx, 6]
    display_dict['pNN25'] = df[_idx, 7]
    display_dict['pNN50'] = df[_idx, 8]
    return df[_idx, :].tolist()


# Load the model
model = joblib.load('models' + os.sep + 'model_sub' + str(subject_id) + '.pkl')

# Replace your URL here. Don't forget to replace the password.
connection_url = 'mongodb+srv://MentalMAIntain:ayon@mentalmaintain.toc5g.mongodb.net/MentalMAIntain?retryWrites=true&w=majority'
app = Flask(__name__)
CORS(app)
client = pymongo.MongoClient(connection_url)
app.config['CORS_HEADERS'] = 'Content-Type'

# Database
Database = client.get_database('MentalMAIntain')
# Table
StressData = Database.StressData

# To insert a single document into the database,
# insert_one() function is used
@app.route('/insert-one', methods=['POST'])
def insertOne():
    body = json.loads(request.data)
    timestamp = body["timestamp"]
    data = body["data"]
    condition = body["label"]
    queryObject = {
        'timestamp': timestamp,
        'data': data,
        'condition': condition,
        'user_labelled': False,
    }
    query = StressData.insert_one(queryObject)
    return json.dumps({"success": True}), 200

# To find the first document that matches a defined query,
# find_one function is used and the query to match is passed
# as an argument.
@app.route('/find-one/<argument>/<value>', methods=['GET'])
def findOne(argument, value):
    queryObject = {argument: value}
    query = StressData.find_one(queryObject)
    query.pop('_id')
    return jsonify(query)

@app.route('/delete-one/<argument>/<value>', methods=['GET'])
def deleteOne(argument, value):
    queryObject = {argument: value}
    query = StressData.delete_one(queryObject)
    return jsonify(query)

@app.route('/dummy', methods=['GET'])
def dummy():
    return jsonify([{"1": 1, "word": "hello"}, {"1": 2, "word": "goodbye"}])


# To find all the entries/documents in a table/collection,
# find() function is used. If you want to find all the documents
# that matches a certain query, you can pass a queryObject as an
# argument.
@app.route('/find', methods=['GET'])
def findAll():
    # user_labelled
    query = StressData.find()
    output = []
    i = 0
    for x in query:
        if not x['user_labelled']:
            output.append(x)
            output[i].pop('_id')
            i += 1
    return jsonify(output)


# To update a document in a collection, update_one()
# function is used. The queryObject to find the document is passed as
# the first argument, the corresponding updateObject is passed as the
# second argument under the '$set' index.
@app.route('/update', methods=['POST'])
# key: 'timestamp'; element: 'condition'; updateValue: 'stress' or 'baseline' entered by user
def update():
    body = json.loads(request.data)
    key = body["key"]
    value = body["value"]
    element = body["element"]
    updateValue = body["updateValue"]
    queryObject = {key: value}
    updateObject = {element: updateValue}
    query = StressData.update_one(queryObject, {'$set': updateObject})
    if query.acknowledged:
        return "Update Successful"
    else:
        return "Update Unsuccessful"


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

    display_dict.update({"label": output,
                         "timestamp": now.strftime("%Y-%m-%d %H:%M:%S")})
    return json.dumps(display_dict), 200

    # TODO:  call insert_one() to store the predicted data for user labelling
    # TODO: When user labels a data
    #  1. Call update first for http://0.0.0.0:8080/update/timestamp/../condition/..
    #  2. Call update first for http://0.0.0.0:8080/update/timestamp/../user_labelled/True/
    # TODO: Call findall() for displaying unlabelled data to the client

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=int(os.environ.get("PORT", 8080)))
