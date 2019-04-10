import socket

'''A kind socket that sends and receives strings'''
class StringSocket(object):
    def __init__(self, skt=None):
        if (skt):
            self.skt = skt
        else:
            self.skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self, host, port):
        self.skt.connect((host, port))

    def bind(self, host, port):
        self.skt.bind((host, port))

    def listen(self):
        self.skt.listen()

    def accept(self):
        new_skt, addr = self.skt.accept()
        return StringSocket(new_skt), addr

    def sendall(self, msg):
        self.skt.sendall(msg.encode())

    def send_with_size(self, msg):
        self.skt.sendall(str(len(msg)).zfill(3).encode())
        self.skt.sendall(msg.encode())

    def receiveall(self, msg_len):
        msg = ""
        while len(msg) < msg_len:
            chunk = self.skt.recv(msg_len-len(msg))
            if not chunk:
                raise RuntimeError('Lal')
            msg = msg + chunk.decode('UTF-8', 'ignore')
        print("-----------Recibi un mensaje: {}-----------".format(msg))
        return msg

    def receive_with_size(self, size_field_size):
        field_size = self.receiveall(size_field_size)
        return self.receiveall(int(field_size))

    def close(self):
        self.skt.close()
