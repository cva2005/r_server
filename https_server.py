from http.server import HTTPServer, SimpleHTTPRequestHandler
import ssl

context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain(certfile='ca_cert.pem', keyfile='ca_key.pem')
context.check_hostname = False

with HTTPServer(("192.168.1.117", 9001), SimpleHTTPRequestHandler) as httpd:
    httpd.socket = context.wrap_socket(httpd.socket, server_side=True)
    httpd.serve_forever()
