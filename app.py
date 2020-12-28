from flask import Flask, url_for, render_template, redirect
from forms import PredictForm
from flask import request, sessions
import requests
from flask import json
from flask import jsonify
from flask import Request
from flask import Response
import urllib3
import json
# from flask_wtf import FlaskForm

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.secret_key = 'development key'  # you will need a secret key


@app.route('/', methods=('GET', 'POST'))
def startApp():
    form = PredictForm()
    return render_template('index.html', form=form)


@app.route('/predict', methods=('GET', 'POST'))
def predict():
    form = PredictForm()
    if form.submit():

        # NOTE: generate iam_token and retrieve ml_instance_id based on provided documentation
        header = {'Content-Type': 'application/json', 'Authorization': 'Bearer '
                  + "eyJraWQiOiIyMDIwMTIyMTE4MzQiLCJhbGciOiJSUzI1NiJ9.eyJpYW1faWQiOiJJQk1pZC01NTAwMDlRSkRNIiwiaWQiOiJJQk1pZC01NTAwMDlRSkRNIiwicmVhbG1pZCI6IklCTWlkIiwianRpIjoiOTU3OTRlMWMtMjQyYy00ZTY1LTkyYzQtNGU4ZTc1OGRlODU0IiwiaWRlbnRpZmllciI6IjU1MDAwOVFKRE0iLCJnaXZlbl9uYW1lIjoiQXlvbiIsImZhbWlseV9uYW1lIjoiQm9ydGhha3VyIiwibmFtZSI6IkF5b24gQm9ydGhha3VyIiwiZW1haWwiOiJhYjI1MzVAY29ybmVsbC5lZHUiLCJzdWIiOiJhYjI1MzVAY29ybmVsbC5lZHUiLCJhY2NvdW50Ijp7InZhbGlkIjp0cnVlLCJic3MiOiJkMTZmNDNkYmE3Zjg0MWViOTIyZWI1Y2Q1ZWQwN2Q0YSIsImZyb3plbiI6dHJ1ZX0sImlhdCI6MTYwOTEyMzEzOCwiZXhwIjoxNjA5MTI2NzM4LCJpc3MiOiJodHRwczovL2lhbS5ibHVlbWl4Lm5ldC9pZGVudGl0eSIsImdyYW50X3R5cGUiOiJ1cm46aWJtOnBhcmFtczpvYXV0aDpncmFudC10eXBlOmFwaWtleSIsInNjb3BlIjoiaWJtIG9wZW5pZCIsImNsaWVudF9pZCI6ImRlZmF1bHQiLCJhY3IiOjEsImFtciI6WyJwd2QiXX0.txtfOqWKc7iPRvPMglur0CNyZw69nDar3RDPj67CFF1ai-Vms7Wklzve9JawoD8pDmYdHSurAeUWRk05fowhW6l93TSOb_3LWcjb0RcvZcKY1j02JDpCoy0xLVVJDCnb1vImbnCepohY7LGqdrH-W82Rha2CUJcCtjCr3mXQmwWwuigyIjBLvkwzTdcgIaKzoBQ-AqGcHE4OeQ1rXv3jBTiq33vW1EZgbYb9gTmjJM1UM2w3dNag7x1QhTKOqCzcSK_Tk9pH80SS3ree09QRvLtCkW5Kfg71nsTL30G5drsJraE8w3mlsU9UcrHyhHI9IYN914G7XyfNsVJ5JNJfEA", "refresh_token": "OKBo6J5fAhbVMxB-I3izNIR3T_PLBr19soq4d2gaSjNeui2hpt33BXreGO0L8f_7Mu0y3ymYEVZHPJUhS4hR9Kd7nv3awLP-Rm-fRyGp-nwD2_T9X15Av_2LnQyMbop1pmqOXoJe8xr_Milsd04xBAEQRqQJ1EklwCWXQ5MZCHdkR1i1H9kvnxPIS48nEBLPr3ddTggdMoxVNtC9VIYBPXZool3ckZPkLpHFtHlVlcZsWql-01IYrUF98eK9IPMUd7GZdOWug322GsWb_0zj7hDE1zjFPzdawMYz1zgNo_6QbwwDo5ouUHilRDAVSDWaDCqvaGJeYsH4_BgA5z4rjPV80R3zAkcMC8f8DqRKKMMosSJCX7F2EyWDExdD2LTorGVjIfgf9L3WnnFuoLDwvYRwp0Au0wbYO5VN-SQXWfwqn7DuPiC8ILaxJFBi0Ql5iGZA0zd9KPDoc4QWWZwTc9WFXRvhg7a8xwO6O66SeLomX1dqzyCOTFOQgHysL5GkdlXbwHCuCd1xq9e6sGiGz1wsXeK3rtLbn0To9aNnNfwjjTfLhJBsrsv28h-Ml3dY52KG9iFsY30tI1P8LdVWOWtCs9ylQoIkx42utqFsb2eTVwP3QZmqK6dsTakhUeQ_HK38jtDepEuYGM5sRVVqwUX4Q3frMIHiCsiIGhCb2TYEmaImWyP1tRTZAxUKeNtkRgloZd7VGI9-apMKqYZnbb8Udy7eB7kV2dXC3x4ArL0jklCkA3-YmrDPASeOEz1o8aIhyNVqRgjfxuUf4qzkiA5jklhLmn0xXTSvof6BijyWnGg5n6fwD4Cgacb7tzzdKZi2qFO0_oVOX0ICmKm7DAqCiTAyQIN1ELEWXH3d-k4S6T74RI3HJ2oGtPC-P4MwJHOmAZE9SK-Ec2lBKj86e9UKJ4oB3dOHSD_vsNe7gwtq7-_twS1974MQHofK0Yj-Tw779qlAJAF6B6ZBKFioHv7nc6cKOHLPi1DhmM_5FYhTKZ59c7ev_bMJPAjHAi_GKY3w7gP1qIpQxjwm9phd3bIS6qu3NJrrT3oghtpKSEeBeRYl2_pte_wdXv9cKR44Qx95PxKmq3x9sIOSQ2e3XcsukOrsGDoOM58xaUkj0Q-VUw"}

        if(form.bmi.data == None):
            python_object = []
        else:
            python_object = [float(form.MEAN_RR.data), float(form.MEDIAN_RR.data), float(form.SDRR.data),
                             float(form.RMSSD.data), float(
                                 form.SDSD.data), float(form.SDRR_RMSSD.data),
                             float(form.HR.data), float(
                                 form.pNN25.data), float(form.pNN50.data),
                             float(form.SD1.data), float(
                                 form.SD2.data), float(form.KURT.data),
                             float(form.SKEW.data), float(
                                 form.MEAN_REL_RR.data), float(form.MEDIAN_REL_RR.data),
                             float(form.SDRR_REL_RR.data), float(
                                 form.RMSSD_REL_RR.data), float(form.SDSD_REL_RR.data),
                             float(form.SDRR_RMSSD_REL_RR.data), float(
                                 form.KURT_REL_RR.data), float(form.SKEW_REL_RR.data),
                             float(form.VLF.data), float(
                                 form.LF.data), float(form.HF.data),
                             float(form.LF_HF.data), float(form.HF_LF.data)]
        # Transform python objects to  Json

        userInput = []
        userInput.append(python_object)

        # NOTE: manually define and pass the array(s) of values to be scored in the next line
        payload_scoring = {"input_data": [{"fields": ["MEAN_RR", "MEDIAN_RR", "SDRR",
                                                      "RMSSD", "SDSD", "SDRR_RMSSD",
                                                      "HR", "pNN25", "pNN50",
                                                      "SD1", "SD2", "KURT",
                                                      "SKEW", "MEAN_REL_RR", "MEDIAN_REL_RR",
                                                      "SDRR_REL_RR", "RMSSD_REL_RR", "SDSD_REL_RR",
                                                      "SDRR_RMSSD_REL_RR", "KURT_REL_RR", "SKEW_REL_RR",
                                                      "VLF", "LF", "HF",
                                                      "LF_HF", "HF_LF"], "values": userInput}]}

        response_scoring = requests.post(
            "https://us-south.ml.cloud.ibm.com/ml/v4/deployments/b562586b-5af2-4636-b925-464b2be3486c/predictions?version=2020-12-26", json=payload_scoring, headers=header)

        output = json.loads(response_scoring.text)
        print(output)
        for key in output:
            ab = output[key]

        for key in ab[0]:
            bc = ab[0][key]

        roundedCharge = round(bc[0][0], 2)

        form.abc = roundedCharge  # this returns the response back to the front page
        return render_template('index.html', form=form)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
