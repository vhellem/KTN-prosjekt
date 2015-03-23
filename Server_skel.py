# -*- coding: utf-8 -*-
import SocketServer

import json
import re
import datetime
import time

usernames = []
errorLogin = "This username is already being used. Please select a new name or check if you are already logged in."
backlog = []
connections = []
helpText = "Commands: Press login <username> to log in. Type a message to send. Type names to get connected users. Type help to get this help text. Type logout to log out."
class ClientHandler(SocketServer.BaseRequestHandler):
    """
    This is the ClientHandler class. Everytime a new client connects to the
    server, a new ClientHandler object will be created. This class represents
    only connected clients, and not the server itself. If you want to write
    logic for the server, you must write it outside this class
    """

    def handle(self):
        """
        This method handles the connection between a client and the server.
        """
        self.ip = self.client_address[0]
        self.port = self.client_address[1]
        self.connection = self.request
        self.logged_in = False
        self.username = ""
        self.response = {
            'timestamp': '',
            'sender': '',
            'response': '',
            'content': ''
        }

        print "Client connected" + self.ip + ':' + str(self.port)

        # Loop that listens for messages from the client
        while True:
            received_string = self.connection.recv(4096).strip()
            if(received_string):

                data = json.loads(received_string)
                request = data["request"]
                if request == "login":
                    self.login(data["content"])
                elif request == 'help':
                    self.help()
                elif not self.logged_in:
                    self.response['timestamp'] = self.getTimeStamp()
                    self.response['sender'] =   self.username
                    self.response['response'] = 'error'
                    self.response['content'] = "You can not use that command when you are not logged in"
                    self.sendMessage(self.response)

                elif(request == "names"):
                    self.names()
                elif(request == "msg"):
                    self.message(data["content"])
                elif(request == "logout"):
                    self.logout()


    def getTimeStamp(self):
        return str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    def sendHistory(self):

        for message in backlog:

            self.sendMessage(message)
            time.sleep(0.1)

    def sendMessage(self, data):
        self.connection.sendall(json.dumps(data))

    def help(self):

        self.response['timestamp'] = self.getTimeStamp()
        self.response['sender'] =   self.username
        self.response['response'] = 'info'
        self.response['content'] = helpText
        self.sendMessage(self.response)



    def message(self, message):
        self.response['timestamp'] = self.getTimeStamp()
        self.response['sender'] = self.username
        self.response['response'] = 'message'
        self.response['content'] = message
        history = {'timestamp': self.getTimeStamp(), 'sender' : self.username, 'response': 'history', 'content': '' + message}
        backlog.append(history)
        for client in connections:
            client.sendMessage(self.response)


    def logout(self):
        connections.remove(self)
        self.logged_in = False
        self.response['timestamp'] = self.getTimeStamp()
        self.response['sender'] =  self.username
        self.response['response'] = 'info'
        self.response['content'] = 'Logged out ' + self.username
        self.sendMessage(self.response)

    def names(self):
        self.response['timestamp'] = self.getTimeStamp()
        self.response['sender'] = self.username
        self.response['response'] = 'info'
        names = ""
        for name in usernames:
            names += name + ", "
        self.response['content'] = names
        self.sendMessage(self.response)


    def login(self, username):
        if(not re.match(r'^[A-Za-z0-9]+$', username)):
            self.response['timestamp'] = self.getTimeStamp()
            self.response['sender'] = ''
            self.response['response'] = 'error'
            self.response['content'] = 'Invalid username: ' + username
            self.sendMessage(self.response)
        if (username not in usernames):
            self.response['timestamp'] = self.getTimeStamp()
            self.response['sender'] = self.username
            self.response['response'] = 'info'
            self.username = username
            usernames.append(username)
            connections.append(self)
            self.response['content'] = "You have successfully logged in. Welcome!"
            self.sendHistory()
            self.sendMessage(self.response)
            self.logged_in = True
        else:
            self.response['timestamp'] = self.getTimeStamp()
            self.response['sender'] = self.username
            self.response['response'] = 'error'
            self.response['content'] = errorLogin
            self.sendMessage(self.response)




class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    """
    This class is present so that each client connected will be ran as a own
    thread. In that way, all clients will be served by the server.

    No alterations is necessary
    """
    allow_reuse_address = True

if __name__ == "__main__":
    """
    This is the main method and is executed when you type "python Server.py"
    in your terminal.

    No alterations is necessary
    """
    HOST, PORT = 'localhost', 9998
    print 'Server running...'

    # Set up and initiate the TCP server
    server = ThreadedTCPServer((HOST, PORT), ClientHandler)
    server.serve_forever()
