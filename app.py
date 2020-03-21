"""
Author: bishwarup
Created: Friday, 18th March 2020 10:20:55 am
Modified: Friday, 20th March 2020 2:44:13 pm [bishwarup]
"""

import json
from flask import Flask, jsonify, g
from update import Update

app = Flask(__name__)


@app.route("/v1/states", methods=["GET"])
def states():
    updater = Update("https://www.mohfw.gov.in/")
    history = updater.update()
    return jsonify(history)


@app.route("/v1/overall", methods=["GET"])
def overall():
    updater = Update("https://www.mohfw.gov.in/")
    oa = updater.get_overall()
    return jsonify(oa)


if __name__ == "__main__":
    app.run()
