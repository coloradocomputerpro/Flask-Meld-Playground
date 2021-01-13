import names
from flaskapp.forms import ChatInputForm
from flask_meld.component import Component


class Chat(Component):
    #form = ChatInputForm()
    text = ""
    name = names.get_first_name()

    messages = []

    def clear_text(self):
        self.text = ""

    def random_name(self):
        self.name = names.get_first_name()

    def send_message(self):
        message = {}
        if (self.text != "" and self.text is not None):
            message['text'] = self.text
            message['user'] = self.name
            message['valid'] = True
        else:
            fullname = names.get_full_name()
            message['text'] = f"Hello everyone, my name is {fullname}"
            message['user'] = fullname.split()[0]
        self.messages.append(message)
        self.text = ""