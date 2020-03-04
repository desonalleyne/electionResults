import getpass
from fbchat import Client
from fbchat.models import Message,ThreadType, ThreadColor
import os
pw = os.environ['_PW_VAR_']


class Messenger(object):
    def __init__(self):
        self.client = Client("username.@email.com", pw)
    def send(self, userId, message):
        self.client.send(Message(text=message),thread_id='YOUR_ID_HERE',thread_type=ThreadType.USER)

    def logout(self):
        self.client.logout()
