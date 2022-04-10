from distutils.log import debug
import os
import sqlite3

from flask import Flask, flash, redirect, render_template, request
from tempfile import mkdtemp

from flask_mail import Mail, Message

app = Flask(__name__)

# Requires that "Less secure app access" be on
# https://support.google.com/accounts/answer/6010255
app.config["MAIL_DEFAULT_SENDER"] = os.environ["MAIL_DEFAULT_SENDER"]
app.config["MAIL_PASSWORD"] = os.environ.get("MAIL_PASSWORD")
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_TLS"] = False
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_USERNAME"] = os.environ["MAIL_USERNAME"]

mail = Mail(app)

# Create a Connection
connection = sqlite3.connect("database.db", check_same_thread=False)

# Create a Cursor
db = connection.cursor()
#db.execute("create table form (customer_name text, customer_address text, customer_number text, church_pastor text, sermon_name text, sermon_pastor text, order_type text)")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        customer_name = request.form.get("name")
        customer_address = request.form.get("address")
        customer_number = request.form.get("number")
        order_type = request.form.get("type")

        church_pastor = request.form.get("ch_pastor")
        sermon_name = request.form.get("sermon")
        sermon_pastor = request.form.get("se_pastor")

        #db.execute("INSERT INTO form (customer_name , customer_address, customer_number, church_pastor, sermon_name, sermon_pastor, order_type) VALUES(?, ?, ?, ?, ?, ?, ?)", [customer_name , customer_address, customer_number, church_pastor, sermon_name, sermon_pastor, order_type])

        email_body = "Customer Name: " + customer_name, "/nCustomer Address: " + customer_address, "/nCustomer Number: " + customer_number, "Order Type: " + order_type, "/nCustomer Pastor: " + church_pastor, "/nSermon Name: " + sermon_name, "/nSermon Pastor: " + sermon_pastor

        # Send email
        
        message = Message(email_body, recipients=[os.environ.get("email")])
        mail.send(message)
        return redirect("/")
    else:
        return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)


    