from flask import Flask, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_mail import Mail, Message
from dotenv import load_dotenv
import os

load_dotenv()

db = SQLAlchemy()
mail = Mail()


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "default-dev-key")
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI", "sqlite:///data.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.getenv("EMAIL")
    MAIL_PASSWORD = os.getenv("PASSWORD")
    MAIL_DEFAULT_SENDER = os.getenv("EMAIL")


class FormSubmission(db.Model):
    __tablename__ = "form_submissions"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    date = db.Column(db.Date, nullable=False)
    occupation = db.Column(db.String(80), nullable=False)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        email = request.form["email"]
        date = request.form["date"]
        date_obj = datetime.strptime(date, "%Y-%m-%d")
        occupation = request.form["occupation"]

        form = FormSubmission(
            first_name=first_name,
            last_name=last_name,
            email=email,
            date=date_obj,
            occupation=occupation,
        )

        db.session.add(form)
        db.session.commit()

        message_body = (
            f"Thank you for your submission, {first_name}. "
            f"Here are your data:\n{first_name}\n{last_name}\n{date}\n"
            f"Thank you!"
        )
        message = Message(
            subject="New form submission",
            sender=app.config["MAIL_USERNAME"],
            recipients=[email],
            body=message_body,
        )

        mail.send(message)

        flash(f"{first_name}, your form was submitted successfully", "success")

    return render_template("index.html")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        app.run(debug=True, port=5001)
