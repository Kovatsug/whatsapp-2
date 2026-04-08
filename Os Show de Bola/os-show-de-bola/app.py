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
from entities.User import User

app = Flask(__name__)
app.secret_key = "sdidisfusdhfufhabcdefg"


users = [
    User("pablo", "0000"),
    User("maximiliano", "0000"),
]


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
                user.name.lower() == form.name.data.lower()
                and user.password == form.password.data
            ):
                session["user"] = user
                return redirect(url_for("telaLogado"))

    return render_template("index.html", form=form)


@app.route("/logado", methods=["POST", "GET"])
def telaLogado():

    if "user" in session:
        logout = Logout()
        if logout.validate_on_submit():
            session.pop("user", None)
            return redirect(url_for("home"))

        addContactForm = AddContactForm()
        if addContactForm.validate_on_submit():
            contactName = addContactForm.contactName.data

            for user in users:
                if contactName == user.name:
                    session["user"].addContact(contactName)

            print(session["user"])

        return render_template(
            "logado.html", logout=logout, addContactForm=addContactForm
        )
    else:
        return redirect(url_for("home"))


class Logout(FlaskForm):
    submit = SubmitField("Sair")


class AddContactForm(FlaskForm):
    contactName = StringField("Contato:", validators=[DataRequired()])
    submit = SubmitField("Adicionar")


if __name__ == "__main__":
    app.run(debug=True)
