from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class SendMessageForm(FlaskForm):
    message_field = StringField("Mensagem: ", validators=[DataRequired()])
    submit_send_message = SubmitField("Enviar")
