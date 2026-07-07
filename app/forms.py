from flask_wtf import FlaskForm
from wtforms import StringField, DateField, RadioField
from wtforms.validators import DataRequired, Email, Length


class JobApplicationForm(FlaskForm):
    first_name = StringField(
        "First Name", validators=[DataRequired(), Length(min=2, max=80)]
    )
    last_name = StringField(
        "Last Name", validators=[DataRequired(), Length(min=2, max=80)]
    )
    email = StringField(
        "Email", validators=[DataRequired(), Email(message="Invalid email address.")]
    )
    date = DateField("Available Start Date", validators=[DataRequired()])
    occupation = RadioField(
        "Occupation",
        choices=[
            ("employed", "Employed"),
            ("unemployed", "Unemployed"),
            ("self-employed", "Self-Employed"),
            ("student", "Student"),
        ],
        validators=[DataRequired()],
    )
