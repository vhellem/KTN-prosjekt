# -*- coding: utf-8 -*-
import socket
import threading
import re
import json
import sys



from MessageReceiver import ReceiveMessageWorker


class Client:
    """
    This is the chat client class
    """

    def __init__(self, host, server_port):
        """
        This method is run when creating a new Client object
        """
         # Set up the socket connection to the server
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.run(host, server_port)

        # TODO: Finish init process with necessary code
        #Vegard sier vi ikke skal skrive noe her
        

        
    def run(self, host, server_port):
        # Initiate the connection to the server
        self.connection.connect((host, server_port))
        messageWorker = ReceiveMessageWorker(self, self.connection)
        messageWorker.start()
        while True:
            input_data = str(raw_input('Input: '))
            inputsplit = input_data.split(" ", 1)
            if inputsplit[0] == 'login':
                if len(inputsplit) == 1:
                    print("Vennligst skriv brukernavn etter 'login'")
                else:
                    self.login(
                        inputsplit[1])
            elif inputsplit[0] == 'help':
                self.help_plz()
            elif inputsplit[0] == 'names':
                self.names()
            elif inputsplit[0] == 'logout':
                self.logout()
            else:
                self.message(input_data)
        


    def login(self, username):
        d = {}
        d['request'] = 'login'
        d['content'] = username
        self.send( d)
        
    def help_plz(self):
        d = {}
        d['request'] = 'help'
        d['content'] = None
        self.send(d)
        
    def message(self, message):
        d = {}
        d['request'] = 'msg'
        d['content'] = message
        self.send(d)
        
    def names(self):
        d = {}
        d['request'] = 'names'
        d['content'] = None
        self.send(d)
        
    def logout(self):
        d = {}
        d['request'] = 'logout'
        d['content'] = None
        self.send(d)



    
    def send(self, request):

        json_request = json.dumps(request)
        self.connection.sendall(json_request)

    def message_received(self, message, connection):
        request = json.loads(message)
        response = request["response"]
        content = request["content"]
        sender = request["sender"]
        timestamp = request["timestamp"]

        if (response == 'info'):
            print content
        elif (response == 'error'):
            print content
        elif (response == 'message'):
            message = "" + timestamp + ": " + sender + ": " + content
            print message
        elif (response == 'history'):
            message = "" + timestamp + ": " + sender + ": " + content
            print message

  

if __name__ == '__main__':
    """
    This is the main method and is executed when you type "python Client.py"
    in your terminal.

    No alterations is necessary
    """
    client = Client('localhost', 9998)
