from flask import (
    Flask,
    render_template,
    redirect,
    url_for,
    session,
)
from entities.User import User
from entities.Message import Message
from forms.LoginForm import LoginForm
from forms.AddContactForm import AddContactForm
from forms.LogoutButton import LogoutButton
from forms.SendMessageForm import SendMessageForm

app = Flask(__name__)
app.secret_key = "sdidisfusdhfufhabcdefg"

users = [
    User("pablo", "0000", ["maximiliano"]),
    User("maximiliano", "0000", ["pablo"]),
]

messages = [
    Message("pablo", "maximiliano", "oi"),
    Message("maximiliano", "pablo", "olá"),
]


def getUser(name):
    for user in users:
        if user.name == name:
            return user


def userExists(name):
    for user in users:
        if user.name == name:
            return True

    return False


@app.route("/", methods=["GET", "POST"])
def loginPage():
    login_form = LoginForm()

    if login_form.validate_on_submit():
        for user in users:
            if (
                user.name.lower() == login_form.name.data.lower()
                and user.password == login_form.password.data
            ):
                session["user"] = user.name
                return redirect(url_for("homePage"))

    return render_template("login.html", login_form=login_form)


@app.route("/home", methods=["GET", "POST"])
def homePage():
    if not ("user" in session):
        return redirect(url_for("loginPage"))

    logout_button = LogoutButton()
    add_contact_form = AddContactForm()

    if logout_button.submit_logout.data and logout_button.validate():
        session.pop("user", None)
        return redirect(url_for("loginPage"))

    if add_contact_form.submit_add_contact.data and add_contact_form.validate():
        contact_name = add_contact_form.contact_name.data

        if not userExists(contact_name):
            print("não existente")
        else:
            logged_user = getUser(session["user"])
            logged_user.add_contact_name(contact_name)
            print(logged_user)
            print("Contato adicionado")

    return render_template(
        "home.html", logout_button=logout_button, add_contact_form=add_contact_form
    )


@app.route("/chat/<contact_name>", methods=["GET", "POST"])
def chatPage(contact_name):
    if not ("user" in session):
        return redirect(url_for("loginPage"))

    logged_user = getUser(session["user"])

    isContactValid = False
    for contact in logged_user.contact_names:
        if contact == contact_name:
            isContactValid = True

    if not isContactValid:
        return "Contato não encontrado"

    send_message_form = SendMessageForm()

    if send_message_form.validate_on_submit():
        message_content = send_message_form.message_field.data
        messages.append(Message(logged_user.name, contact_name, message_content))

        return redirect(url_for("chatPage", contact_name=contact_name))

    messages_to_show = []

    for message in messages:
        if (
            message.sender_name == logged_user.name
            and message.receiver_name == contact_name
        ) or (
            message.sender_name == contact_name
            and message.receiver_name == logged_user.name
        ):
            messages_to_show.append(message)

    return render_template(
        "chat.html",
        send_message_form=send_message_form,
        messages_to_show=messages_to_show,
    )


if __name__ == "__main__":
    app.run(debug=True)
