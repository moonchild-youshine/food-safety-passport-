from flask import Flask, render_template, redirect, url_for
import qrcode
import os

app = Flask(__name__)

def create_qr(batch_id):
    url = f"http://food-safety-passport.onrender.com/product/{batch_id}"

    img = qrcode.make(url)

    base_folder = os.path.dirname(os.path.abspath(__file__))
    qr_folder = os.path.join(base_folder, "static", "qr")

    os.makedirs(qr_folder, exist_ok=True)

    qr_file = os.path.join(qr_folder, batch_id + ".png")
    img.save(qr_file)

    print("QR CREATED:", qr_file)

# Sample food products
products = {
    "VS26092001": {
        "name": "Veg Sandwich",
        "prepared": "20 September 2026, 10:30 AM",
        "packed": "20 September 2026, 10:45 AM",
        "use_by": "21 September 2026",
        "storage": "Keep refrigerated",
        "allergens": "Milk, Wheat",
        "status": "safe",
        "status_text": "WITHIN RECORDED CONDITIONS",
        "journey": [
            ("🥪", "Prepared", "20 Sep • 10:30 AM"),
            ("📦", "Packaged", "20 Sep • 10:45 AM"),
            ("❄️", "Cold Storage", "20 Sep • 11:00 AM"),
            ("🚚", "Dispatched", "20 Sep • 1:00 PM"),
            ("🏪", "Delivered", "20 Sep • 2:00 PM")
        ]
    },

    "VS26092002": {
        "name": "Veg Sandwich",
        "prepared": "20 September 2026, 11:00 AM",
        "packed": "20 September 2026, 11:15 AM",
        "use_by": "21 September 2026",
        "storage": "Keep refrigerated",
        "allergens": "Milk, Wheat",
        "status": "alert",
        "status_text": "CHECK REQUIRED",
        "journey": [
            ("🥪", "Prepared", "20 Sep • 11:00 AM"),
            ("📦", "Packaged", "20 Sep • 11:15 AM"),
            ("❄️", "Cold Storage", "20 Sep • 11:30 AM"),
            ("⚠️", "Temperature Excursion", "20 Sep • 4:12 PM"),
            ("🔍", "Requires Check", "20 Sep • 4:15 PM")
        ]
    },

    "PW26092003": {
        "name": "Paneer Wrap",
        "prepared": "20 September 2026, 12:00 PM",
        "packed": "20 September 2026, 12:15 PM",
        "use_by": "21 September 2026",
        "storage": "Keep refrigerated",
        "allergens": "Milk, Wheat",
        "status": "safe",
        "status_text": "WITHIN RECORDED CONDITIONS",
        "journey": [
            ("🌯", "Prepared", "20 Sep • 12:00 PM"),
            ("📦", "Packaged", "20 Sep • 12:15 PM"),
            ("❄️", "Cold Storage", "20 Sep • 12:30 PM"),
            ("🚚", "Dispatched", "20 Sep • 2:00 PM"),
            ("🏪", "Delivered", "20 Sep • 3:00 PM")
        ]
    }
}


@app.route("/")
def home():
    return render_template("index.html", products=products)


@app.route("/product/<batch_id>")
def passport(batch_id):

    product = products.get(batch_id)

    if product is None:
        return "Product not found", 404

    return render_template(
        "passport.html",
        product=product,
        batch_id=batch_id
    )


@app.route("/dashboard")
def dashboard():
    return render_template(
        "dashboard.html",
        products=products
    )


@app.route("/alert/<batch_id>")
def create_alert(batch_id):

    if batch_id in products:

        products[batch_id]["status"] = "alert"
        products[batch_id]["status_text"] = "CHECK REQUIRED"

        products[batch_id]["journey"].append(
            ("⚠️", "Temperature Excursion", "Demo Event")
        )

    return redirect(url_for("dashboard"))


@app.route("/reset/<batch_id>")
def reset_status(batch_id):

    if batch_id in products:

        products[batch_id]["status"] = "safe"
        products[batch_id]["status_text"] = "WITHIN RECORDED CONDITIONS"

    return redirect(url_for("dashboard"))


@app.route("/report/<batch_id>")
def report_issue(batch_id):

    if batch_id in products:

        products[batch_id]["status"] = "alert"
        products[batch_id]["status_text"] = "CHECK REQUIRED"

    return redirect(url_for("passport", batch_id=batch_id))
    
    
    
    
    
    
create_qr("VS26092001")
create_qr("VS26092002")
create_qr("PW26092003")

if __name__ == "__main__":
    app.run( debug=True)
    
    
      
