RECORD_SIZE = 512
from autobahn.twisted.websocket import WebSocketServerProtocol, \
    WebSocketServerFactory

class MyServerProtocol(WebSocketServerProtocol):
    def onConnect(self, request):
        print("Client connecting: {0}".format(request.peer))

    def onOpen(self):
        print("WebSocket connection open.")

    def onMessage(self, payload, isBinary):
        if isBinary:
            ser: int = payload[1] * 256 + payload[0]
            print("Binary message received: {0}".format(ser))
            import glob
            f_name = glob.glob('8RS-1ETH-GTW*.bin')
            len = os.path.getsize(f_name[0])
            print("Binary message Send: {0}".format(len))
            buf: bytearray = bytearray(len)
            with open(f_name[0], 'rb') as f:
                f.readinto(buf)
            s_buf: bytes = bytes(0)
            s_buf = s_buf + buf
            self.sendMessage(s_buf, isBinary)
        else:
            str_id = payload.decode('utf8')
            print("Text message received: {0}".format(str_id))
            import glob
            if str_id == "MB_IEC_GTW":
                f_name = glob.glob('MB_IEC_GTW*.bin')
            else:
                f_name = glob.glob('8RS-1ETH-GTW*.bin')
            self.sendMessage(bytes(f_name[0], 'utf-8'))
            print("File Name Send Complete")

        # echo back message verbatim
        #self.sendMessage(payload, isBinary)

    def onClose(self, wasClean, code, reason):
        print("WebSocket connection closed: {0}".format(reason))


if __name__ == '__main__':

    import sys
    import os.path

    from twisted.python import log
    from twisted.internet import reactor
    from functools import partial
    from requests import get

    log.startLogging(sys.stdout)


    ip = get('https://api.ipify.org').text
    print('My public IP address is: {}'.format(ip))
    ip = "192.168.1.117"

    factory = WebSocketServerFactory("ws://" + ip + ":9000")
    factory.protocol = MyServerProtocol
    # factory.setProtocolOptions(maxConnections=2)
    # note to self: if using putChild, the child must be bytes...

    reactor.listenTCP(9000, factory)
    reactor.run()