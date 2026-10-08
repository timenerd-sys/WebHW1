import socket
import HTMLParser
from Builder import Builder

def receive(sock):
    received = b''

    while True:
        part = sock.recv(4096)

        if not part:
            break

        received += part
    sock.close()
    return received

s = socket.create_connection(('hw1.alexbers.com', 80))

request = (
    b'GET / HTTP/1.1\r\n'
    b'Host: hw1.alexbers.com\r\n'
    b'Cookie: user=5b1fed3ee3af63040b0ef367963661a5\r\n'
    b'Connection: close\r\n'
)
s.sendall(request)

message = receive(s)

response, html = message.split(b'\r\n\r\n', 1)
parsed_html = HTMLParser.parse(html.decode())

print(response.decode())
print(html.decode())

while True:
    builder = Builder()
    request = builder.build(parsed_html)
    print(repr(request))

    s = socket.create_connection(('hw1.alexbers.com', 80))
    s.settimeout(5)
    s.sendall(bytes(request, 'utf-8'))

    message = receive(s)
    s.close()

    response, html = message.split(b'\r\n\r\n', 1)
    parsed_html = HTMLParser.parse(html.decode())

    print(response.decode())
    print(html.decode())
    print('----------------------------------------------------------------------------------------')