class User:
    def __init__(self, name, password):
        self.contacts = []
        self.name = name
        self.password = password

    def add_contact(self, contact):
        self.contacts.append(contact)

    def __str__(self):
        return self.name + self.password + self.contacts
