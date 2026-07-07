from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_mail import Mail, Message


class FormSubmission(db.Model):
    __tablename__ = "form_submissions"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    date = db.Column(db.Date, nullable=False)
    occupation = db.Column(db.String(80), nullable=False)


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    mail.init_app(app)

    with app.app_context():
        db.create_all()

    @app.route("/", methods=["GET", "POST"])
    def index():
        if request.method == "POST":
            first_name = request.form.get("first_name", "").strip()
            last_name = request.form.get("last_name", "").strip()
            email = request.form.get("email", "").strip()
            date_str = request.form.get("date", "").strip()
            occupation = request.form.get("occupation", "").strip()

            if not all([first_name, last_name, email, date_str, occupation]):
                flash("All fields are required.", "danger")
                return redirect(url_for("index"))

            try:
                date_obj = datetime.strptime(date_str, "%Y-%m-%d")
            except ValueError:
                flash("Invalid date format submitted.", "danger")
                return redirect(url_for("index"))

            try:
                submission = FormSubmission(
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    date=date_obj,
                    occupation=occupation,
                )

                db.session.add(submission)
                db.session.commit()
            except Exception:
                db.session.rollback()
                flash(
                    "An internal error occurred while saving your submission. Please try again.",
                    "danger",
                )
                return redirect(url_for("index"))

            try:
                message_body = (
                    f"Hello {first_name},\n\n"
                    f"Thank you for your submission. Here is a summary of the details we received:\n\n"
                    f"Name: {first_name} {last_name}\n"
                    f"Email: {email}\n"
                    f"Available Start Date: {date_str}\n"
                    f"Current Occupation: {occupation}\n\n"
                    f"Best regards,\nThe Team"
                )
                message = Message(
                    subject="New Form Submission Confirmation",
                    recipients=[email],
                    body=message_body,
                )
                mail.send(message)
            except Exception:
                flash(
                    f"{first_name}, your form was saved, but we couldn't send the confirmation email.",
                    "warning",
                )
                return redirect(url_for("index"))

            flash(f"{first_name}, your form was submitted successfully!", "success")

            return redirect(url_for("index"))

        return render_template("index.html")

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=5001)
