
import json
from flask import Flask, request, render_template
from flask_cors import CORS
import firebase_admin
from firebase_admin import firestore
from flask import send_file
import qrcode


cred_obj = firebase_admin.credentials.Certificate(
    'reformbar-a4b02-firebase-adminsdk-y0re0-40695dbdf0.json')
default_app = firebase_admin.initialize_app(cred_obj)

app = Flask(__name__, static_url_path='/static')
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
    id_official = request.form["id_official"]
    db = firestore.client()

    doc_ref = db.collection(u'customers').document(id)

    data = {
        u'name': name,
        u'dob': dob,
        u'gender': gender,
        u'payment': payment,
        u'height': height,
        u'weight': weight,
        u'drinks': "0",
        u'id_official': id_official
    }
    doc_ref.set(data)
    makeqrcodes(id)
    print("Made qr code")
    return "Made Image"


def makeqrcodes(id):
    import os
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=4,
    )

    qr.add_data(id)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    path_to_save_image = os.path.join(
        os.getcwd(), "static", "id_images", f'{id}.png')
    img.save(path_to_save_image)


@app.route('/')
def serve_login():
    return render_template("login.html")


@app.route('/register')
def serve_register():
    return render_template("index.html")


@app.route('/drink/<variable>', methods=['GET'])
def serve_drinks(variable):
    data = {"drink_id": variable, "abc": "abc"}
    return render_template("qr_code.html", data=data)


@app.route('/add_drink', methods=['POST'])
def add_drink():
    name = request.form["drink"]
    id = request.form["id"]
    db = firestore.client()

    doc_ref = db.collection(u'customers').document(id)
    doc = doc_ref.get()

    drink_ref = db.collection(u'drink').document(name)
    doc_drink = drink_ref.get()

    drink_data = doc_drink.to_dict()
    existing_data = doc.to_dict()
    if existing_data["drinks"] < 3 and int(existing_data["payment"]) > int(drink_data["price"]):

        data = {
            u'drinks': str(int(existing_data["drinks"])+1),
            u'alcohol': str(drink_data["alcohol"]),
            u'payment': str(int(existing_data["drinks"])-int(drink_data["price"]))
        }
        doc_ref.set(data, merge=True)
        return "Successful Order Placed"
    else:
        return "Unsuccessful Order"


if __name__ == "__main__":
    app.run()
