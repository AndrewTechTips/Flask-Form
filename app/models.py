from app.extensions import db


class FormSubmission(db.Model):
    __tablename__ = "form_submissions"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    date = db.Column(db.Date, nullable=False)
    occupation = db.Column(db.String(80), nullable=False)
