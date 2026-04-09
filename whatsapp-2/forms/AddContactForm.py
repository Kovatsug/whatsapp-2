from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class AddContactForm(FlaskForm):
    contact_name = StringField("Contato:", validators=[DataRequired()])
    submit_add_contact = SubmitField("Adicionar")
