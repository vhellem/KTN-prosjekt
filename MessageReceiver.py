
from threading import Thread


class ReceiveMessageWorker(Thread):

    def __init__(self, listener, connection):
        super(ReceiveMessageWorker, self).__init__()
        self.setDaemon(True)
        self.connection = connection
        self.listener = listener

    def run(self):
        while True:
            response = self.connection.recv(1024).strip()
            self.listener.message_received(response, self.connection)