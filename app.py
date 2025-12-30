import pickle
from flask import Flask, request, jsonify, url_for, render_template, app
import numpy as np
import pandas as pd

app = Flask(__name__)
model = pickle.load(open("artifacts/regmodel.pkl", "rb"))
scaler = pickle.load(open("artifacts/scaler.pkl", "rb"))


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/predict_api", methods=["POST"])
def predict_api():
    data = request.json['data']
    print(data)
    print(np.array(list(data.values())).reshape(1, -1))

    new_data = scaler.transform(np.array(list(data.values())).reshape(1, -1))
    output = model.predict(new_data)
    print(output[0])
    return jsonify({"prediction": output[0]})


@app.route("/predict", methods=["POST"])
def predict():
    data = [float(x) for x in request.form.values()]
    final_input = scaler.transform(np.array(data).reshape(1, -1))
    print(final_input)
    output = model.predict(final_input)[0]
    return render_template("home.html", prediction_text=f"The predicted price of the house is ${output*1000:.2f}")

if __name__ == "__main__":
    app.run(debug=True)