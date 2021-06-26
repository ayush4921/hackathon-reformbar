
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
        u'id_official': id_official,
        u'alcohol': "0",
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


@app.route('/bar')
def serve_bar():
    return render_template("menu.html")


@app.route('/drink/<variable>', methods=['GET'])
def serve_drinks(variable):
    data = {"drink_id": variable, "abc": "abc"}
    return render_template("qr_code.html", data=data, drink_name=variable)


@app.route('/add_drink', methods=['POST'])
def add_drink():
    import dateutil
    import datetime
    from dateutil import parser

    name = request.form["drink"]
    id = request.form["id"]
    db = firestore.client()

    doc_ref = db.collection(u'customers').document(id)
    doc = doc_ref.get()

    drink_ref = db.collection(u'drink').document(name)
    doc_drink = drink_ref.get()

    drink_data = doc_drink.to_dict()
    existing_data = doc.to_dict()

    date = parser.parse(existing_data["dob"])
    now = datetime.datetime.utcnow()

    now = now.date()

    # Get the difference between the current date and the birthday
    age = dateutil.relativedelta.relativedelta(now, date)
    age = age.years
    print(existing_data)
    print(drink_data)
    bac = calculate_bac(float(existing_data["drinks"]), float(existing_data["weight"]), existing_data["gender"], alcohol_consumed=float(
        existing_data["alcohol"])+float(drink_data["alcohol"]))
    if bac < 0.07 and float(existing_data["payment"]) > float(drink_data["price"]) and age > 18:
        data = {
            u'drinks': str(float(existing_data["drinks"])+1),
            u'alcohol': str(float(existing_data["alcohol"])+float(drink_data["alcohol"])),
            u'payment': str(float(existing_data["payment"])-float(drink_data["price"]))
        }
        doc_ref.set(data, merge=True)
        return "Successful Order Placed"
    else:
        if bac > 0.07:
            return "Unsuccessful order:  BAC levels too high"
        elif float(existing_data["payment"]) < float(drink_data["price"]):
            return "Unsuccessful order: Not enough money"
        elif age < 18:
            return "Unsuccessful order: Under the legal age of alcohol consumption"
        return "Unsuccessful Order"


def calculate_bac(no_of_drinks, body_weight_in_kg, gender, r=0.55, alcohol_consumed=14):
    if gender == 'male':
        r = 0.68
    return no_of_drinks * alcohol_consumed * 100 / (body_weight_in_kg * r * 1000)


if __name__ == "__main__":
    app.run(debug=True)
