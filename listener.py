import ConfigParser
import os
import requests
import simplejson
from hipchat import Hipchat
import socket
from flask import Flask
from flask import request

class QueueManager(object):
    def __init__(self):
        self.queue = []
        self.queue_index = 1
    def push(self, index, name):
        index = int(index)
        if(index == 1):
            # Reset the queue
            self.queue = []
            self.queue.append(name)
            self.queue_index = 1
        elif(index == self.queue_index+1):
            if name not in self.queue:
                self.queue.append(name)
                self.queue_index = self.queue_index+1
        else:
            self.queue = []
            self.queue_index = 1
        if(self.queue_index == 4):
            q = self.queue
            self.queue = []
            self.queue_index = 1
            return q
        print self.queue
        return None


if __name__ == "__main__":
    config = ConfigParser.ConfigParser()
    config.read("./config")
    room_id =config.get("Room", "ID")
    api_key =config.get("Room", "key")
    hipchat_url = config.get("Hipchat", "URL")
    user_key = config.get("Hipchat", "user_key")

    h = Hipchat(hipchat_url, user_key, api_key, room_id)
    h.delete_all_webhook()
    h.register_webhook("http://{}:5000/".format("192.168.1.140"), "^\d$")
    queue = QueueManager()

    app = Flask(__name__)

    @app.route('/', methods=['POST'])
    def handle_message():
        if request.method == 'POST':
            json= request.get_json()
            message = json['item']['message']['message']
            user = json['item']['message']['from']['name']
            q = queue.push(message,user)
            if (q != None):
                message = ("(boom) {}, {}, {}, {}".format(*q))
                h.send_message(message)
        return "OK"

    app.run(host="0.0.0.0", port=5000)
