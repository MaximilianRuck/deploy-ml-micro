#!/usr/bin/env python
# coding: utf-8

import numpy as np
from flask import Flask
from flask_restful import Resource, Api
from flask_restful import reqparse

from models import lr as lr_model

app = Flask(__name__)
api = Api(app)


class Home(Resource):
    def get(self):
        return {"data": "Hello world"}  # render_template("index.html")


api.add_resource(Home, "/")


parser = reqparse.RequestParser()
parser.add_argument(
    name="income",
    type=int,
    required=True,
    help="Please send monthly income.",
)
parser.add_argument(
    name="h_size",
    required=True,
    type=int,
    help="Please send size of household.",
)


class LrPrediction(Resource):
    def __init__(self):
        self._income = parser.parse_args().get("income", None)
        self._household_size = parser.parse_args().get("h_size", None)

    def get(self):
        int_features = [self._income, self._household_size]
        final_features = [np.array(int_features)]
        prediction = lr_model.predict_lr_model(features=final_features)
        output = round(prediction[0], 2)
        return {"response": 200, "data": dict(expenses_dollar_per_month=output)}


api.add_resource(LrPrediction, "/lr/")


if __name__ == "__main__":
    app.run(debug=True)
