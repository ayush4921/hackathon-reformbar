
import json
from flask import Flask, request
from flask_cors import CORS
import firebase_admin
from firebase_admin import firestore
from flask import send_file
import qrcode


cred_obj = firebase_admin.credentials.Certificate(
    'reformbar-a4b02-firebase-adminsdk-y0re0-40695dbdf0.json')
default_app = firebase_admin.initialize_app(cred_obj)

app = Flask(__name__)
CORS(app)


@app.route("/makeqrcodeandsetupfirebase", methods=["POST"])
def makedatabasefrominfoandreturntheqrcode():
    name = request.form["name"]
    dob = request.form["dob"]
    gender = request.form["gender"]
    payment = request.form["payment"]
    height = request.form["height"]
    weight = request.form["weight"]
    id = request.form["id"]
    db = firestore.client()

    doc_ref = db.collection(u'customers').document(id)
    data = {
        u'name': name,
        u'dob': dob,
        u'gender': gender,
        u'payment': payment,
        u'height': height,
        u'weight': weight,
    }
    doc_ref.set(data)

    makeqrcodes(id)

    return send_file(f'{id}.png', mimetype='image/png')


def makeqrcodes(id):

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=4,
    )

    qr.add_data(id)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(f'{id}.png')


@app.route("/get", methods=["POST"])
def chatbot_response():
    msg = request.form["msg"]
    ints = predict_class(msg, model)
    res = getResponse(ints, intents)
    return res


if __name__ == "__main__":
    app.run(debug=True)
