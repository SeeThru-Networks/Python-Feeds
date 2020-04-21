from Model.ComponentBase import ComponentBase
import socket


# noinspection PyBroadException
class Socket(ComponentBase):

    def __init__(self, target_url, port=80):
        self.target_url = target_url
        self.port = port

    def run(self):
        # Creates a new socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)

        try:
            # Attempts a connection to the socket
            sock.connect((self.target_url, self.port))
            sock.close()
            return True

        except:
            return False
