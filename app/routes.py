from datetime import datetime
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_mail import Message
from app.extensions import db, mail
from app.forms import JobApplicationForm
from app.models import FormSubmission

main_bp = Blueprint("main", __name__)


@main_bp.route("/", methods=["GET", "POST"])
def index():
    form = JobApplicationForm()

    # validate_on_submit() checks if it's a POST request AND if all validators pass
    if form.validate_on_submit():
        try:
            submission = FormSubmission(
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                email=form.email.data,
                date=form.date.data,
                occupation=form.occupation.data,
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
            html_body = render_template("email_confirmation", form=form)

            # Create a plain text fallback for clients that don't support HTML
            text_body = (
                f"Hello {form.first_name.data},\n\n"
                f"Thank you for your submission. Here is a summary of the details we received:\n\n"
                f"Name: {form.first_name.data} {form.last_name.data}\n"
                f"Email: {form.email.data}\n"
                f"Available Start Date: {form.date.data}\n"
                f"Current Occupation: {form.occupation.data}\n\n"
                f"Best regards,\nThe Team"
            )
            message = Message(
                subject="New Form Submission Confirmation",
                recipients=[form.email.data],
                body=text_body,
                html=html_body,  # Injecting the styled template here
            )
            mail.send(message)
        except Exception:
            flash(
                f"{form.first_name.data}, your form was saved, but we couldn't send the confirmation email.",
                "warning",
            )
            return redirect(url_for("main.index"))

        flash(
            f"{form.first_name.data}, your form was submitted successfully!", "success"
        )
        return redirect(url_for("main.index"))

    # If form has errors (e.g. invalid email), flash them automatically
    if form.errors:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"{error}", "danger")

    # Pass the form object to the template
    return render_template("index.html", form=form)
