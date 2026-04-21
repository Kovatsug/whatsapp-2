class User:
    def __init__(self, name, password, contact_names=[]):
        self.name = name
        self.password = password
        self.contact_names = contact_names

    def to_dict(self):
        return {
            "name": self.name,
            "password": self.password,
            "contact_names": self.contact_names,
        }

    def add_contact_name(self, contact_name):
        self.contact_names.append(contact_name)

    def __str__(self):
        return self.name + self.password + str(self.contact_names)
