from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired


class EnterDrug(FlaskForm):
    drug = StringField("Enter Drug Name: ", validators=[DataRequired()])
    # options = SelectField("Choose Drug", choices = [])
    submit = SubmitField("Submit")