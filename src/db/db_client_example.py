import sys
sys.path.append('../')

from common.string_socket import StringSocket

HOST = '127.0.0.1'
WRITER_PORT = 6061        # The port used by the server
READER_PORT = 6071

s = StringSocket()
s.connect(HOST, WRITER_PORT)
s.sendall("00112345004msg1004tag1")
msg = s.receiveall(2)
print("Recibi: "+msg+" al escribir.")
s.close()

s = StringSocket()
s.connect(HOST, READER_PORT)
s.sendall("0011234512345004tag1")

size = int(s.receiveall(5))
print("Recibi "+str(size)+" logs")
for x in range(size):
    appId = s.receiveall(3)
    timestamp = s.receiveall(5)

    msg_size = s.receiveall(3)
    msg = s.receiveall(int(msg_size))

    tags_size = s.receiveall(3)
    tags = s.receiveall(int(tags_size))

    print("El log fue appID: {}, timestamp: {}, msg: {}, tags: {}".format(appId, timestamp, msg, tags))

s.close()
