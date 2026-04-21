class Message:
    def __init__(self, sender_name, receiver_name, content):
        self.sender_name = sender_name
        self.receiver_name = receiver_name
        self.content = content

    def to_dict(self):
        return {
            "sender_name": self.sender_name,
            "receiver_name": self.receiver_name,
            "content": self.content,
        }

    def add_contact_name(self, contact_name):
        self.contact_names.append(contact_name)

    def __str__(self):
        return self.senderName + self.receiverName + str(self.contact_names)
