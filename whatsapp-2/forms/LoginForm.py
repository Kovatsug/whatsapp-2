from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    name = StringField("Usuário:", validators=[DataRequired()])
    password = StringField("Senha:", validators=[DataRequired()])
    submit = SubmitField("Entrar")
