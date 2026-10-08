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

    return received

s = socket.create_connection(('hw1.alexbers.com', 80))
s.sendall(b"""GET / HTTP/1.1
Host: hw1.alexbers.com
Cookie: user=5b1fed3ee3af63040b0ef367963661a5
Connection: close\n
""")

message = receive(s)

response, html = message.split(b'\r\n\r\n', 1)
parsed_html = HTMLParser.parse(html.decode())

print(response.decode())
print(html.decode())

while True:
    builder = Builder()
    s.sendall(bytes(builder.build(parsed_html), 'utf-8'))
    message = receive(s)
    response, html = message.split(b'\r\n\r\n', 1)
    parsed_html = HTMLParser.parse(html.decode())
    print(response.decode())
    print(html.decode())
    print('----------------------------------------------------------------------------------------')