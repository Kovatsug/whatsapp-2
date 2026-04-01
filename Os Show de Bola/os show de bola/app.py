from flask import (
    Flask,
    render_template,
    redirect,
    url_for,
    request,
    make_response,
    session,
)
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.secret_key = "sdidisfusdhfufhabcdefg"


users = [
    {"name": "Pablo", "password": "0000"},
    {"name": "Maximiliano", "password": "0000"},
]
loggedUser = None


class loginForm(FlaskForm):
    name = StringField("Usuário:", validators=[DataRequired()])
    password = StringField("Senha:", validators=[DataRequired()])
    submit = SubmitField("Entrar")


@app.route("/", methods=["GET", "POST"])
def home():

    form = loginForm()

    if form.validate_on_submit():
        for user in users:
            if (
                user["name"] == form.name.data
                and user["password"] == form.password.data
            ):
                loggedUser = user
                return redirect(url_for("telaLogado"))

    return render_template("index.html", form=form)


@app.route("/logado", methods=["GET", "POST"])
def telaLogado():
    print(loggedUser)
    if loggedUser:
        return render_template("logado.html")
    else:
        return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)
