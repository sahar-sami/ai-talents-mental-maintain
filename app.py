import os
import json
from flask import Flask, request
import pandas

app = Flask(__name__)


@app.route('/anomalies')
def get_anomalies():
    df =
