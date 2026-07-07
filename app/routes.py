from datetime import datetime
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_mail import Message
from app.extensions import db, mail
from app.models import FormSubmission

main_bp = Blueprint("main", __name__)


@main_bp.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        first_name = request.form.get("first_name", "").strip()
        last_name = request.form.get("last_name", "").strip()
        email = request.form.get("email", "").strip()
        date_str = request.form.get("date", "").strip()
        occupation = request.form.get("occupation", "").strip()

        if not all([first_name, last_name, email, date_str, occupation]):
            flash("All fields are required.", "danger")
            return redirect(url_for("main.index"))

        try:
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            flash("Invalid date format submitted.", "danger")
            return redirect(url_for("main.index"))

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
            return redirect(url_for("main.index"))

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
            return redirect(url_for("main.index"))

        flash(f"{first_name}, your form was submitted successfully!", "success")
        return redirect(url_for("main.index"))

    return render_template("index.html")
