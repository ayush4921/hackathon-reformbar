
import json
from flask import Flask, render_template, request
from flask_cors import CORS
import firebase_admin
from firebase_admin import firestore

cred_obj = firebase_admin.credentials.Certificate(
    'reformbar-a4b02-firebase-adminsdk-y0re0-40695dbdf0.json')
default_app = firebase_admin.initialize_app(cred_obj)


app = Flask(__name__)
CORS(app)


@app.route("/makeqrcodeandsetupfirebase", methods=["POST"])
def chatbot_response():
    msg = request.form["msg"]
    ints = predict_class(msg, model)
    res = getResponse(ints, intents)
    return res


@app.route("/get", methods=["POST"])
def chatbot_response():
    msg = request.form["msg"]
    ints = predict_class(msg, model)
    res = getResponse(ints, intents)
    return res


if __name__ == "__main__":
    app.run(debug=True)
