import json
from urllib import response
from flask import (
    Flask,
    render_template,
    redirect,
    request,
    url_for,
    session,
)
from entities.User import User
from entities.Message import Message
from forms.AccountForm import AccountForm
from forms.AddContactForm import AddContactForm
from forms.LogoutButton import LogoutButton
from forms.SendMessageForm import SendMessageForm

app = Flask(__name__)
app.secret_key = "sdidisfusdhfufhabcdefg"

users = []
messages = []


def getUser(name):
    users_cookie = request.cookies.get("users")

    for user in json.loads(users_cookie):
        if user["name"] == name:
            return user


def userExists(name):
    users_cookie = request.cookies.get("users")

    if not users_cookie:
        return False

    for user in json.loads(users_cookie):
        if user["name"] == name:
            return True

    return False


def getUsers():
    users_cookie = request.cookies.get("users")

    if users_cookie:
        return json.loads(users_cookie)

    return []


@app.route("/login", methods=["GET", "POST"])
def loginPage():
    print(users)
    account_form = AccountForm()

    if account_form.validate_on_submit():
        for user in getUsers():
            if (
                user["name"].lower() == account_form.name.data.lower()
                and user["password"] == account_form.password.data
            ):
                session["user"] = user["name"]
                return redirect(url_for("homePage"))

    return render_template("login.html", account_form=account_form)


@app.route("/", methods=["GET", "POST"])
def homePage():
    if not ("user" in session):
        return redirect(url_for("loginPage"))

    logout_button = LogoutButton()
    add_contact_form = AddContactForm()

    message = request.args.get("message", "")

    if logout_button.submit_logout.data and logout_button.validate():
        session.pop("user", None)
        return redirect(url_for("loginPage"))

    if add_contact_form.submit_add_contact.data and add_contact_form.validate():
        contact_name = add_contact_form.contact_name.data

        if not userExists(contact_name):
            message = "Usuário não encontrado"
        else:
            user = getUser(contact_name)
            logged_user = User(user["name"], user["password"], user["contact_names"])
            logged_user.add_contact_name(contact_name)

            logged_user_dict = logged_user.to_dict()

            users_cookie = request.cookies.get("users")

            if users_cookie:
                users = json.loads(users_cookie)
                users.append(logged_user_dict)
            else:
                users = [logged_user_dict]

            response = redirect(
                url_for("homePage", message="Contato adicionado com sucesso")
            )
            response.set_cookie("users", json.dumps(users))
            return response

    return render_template(
        "home.html",
        logout_button=logout_button,
        add_contact_form=add_contact_form,
        message=message,
    )


@app.route("/register", methods=["GET", "POST"])
def registerPage():
    account_form = AccountForm()

    if account_form.validate_on_submit():
        name = account_form.name.data
        password = account_form.password.data

        user = User(name, password, contact_names=[])
        user_dict = user.to_dict()

        users_cookie = request.cookies.get("users")

        if users_cookie:
            users = json.loads(users_cookie)
            users.append(user_dict)
        else:
            users = [user_dict]

        response = redirect(url_for("loginPage"))
        response.set_cookie("users", json.dumps(users))

        return response

    return render_template("register.html", account_form=account_form)


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
        message = Message(logged_user.name, contact_name, message_content)
        message_dict = message.to_dict()

        messages_cookie = request.cookies.get("messages")

        if messages_cookie:
            messages = json.loads(messages_cookie)
            messages.append(message_dict)
        else:
            messages = [message_dict]

        response = redirect(url_for("chatPage", contact_name=contact_name))
        response.set_cookie("messages", json.dumps(messages))

        return response

    messages_cookie = request.cookies.get("messages")

    if messages_cookie:
        messages = json.loads(messages_cookie)

    messages_to_show = []

    for message in messages:
        if (
            message["sender_name"] == logged_user.name
            and message["receiver_name"] == contact_name
        ) or (
            message["sender_name"] == contact_name
            and message["receiver_name"] == logged_user.name
        ):
            messages_to_show.append(
                Message(
                    message["sender_name"], message["receiver_name"], message["content"]
                )
            )

    return render_template(
        "chat.html",
        logged_user_name=logged_user.name,
        send_message_form=send_message_form,
        messages_to_show=messages_to_show,
    )


if __name__ == "__main__":
    app.run(debug=True)
