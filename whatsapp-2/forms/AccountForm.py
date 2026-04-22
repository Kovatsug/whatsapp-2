from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired


class AccountForm(FlaskForm):
    name = StringField("Usuário:", validators=[DataRequired()])
    password = PasswordField("Senha:", validators=[DataRequired()])
    submit = SubmitField("Entrar")
