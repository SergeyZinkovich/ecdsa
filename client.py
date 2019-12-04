import socket
from ast import literal_eval
import elliptic_module as el


def verify_signature(public_key, message, signature):
    z = el.hash_message(message)

    r, s = signature

    w = el.inverse_mod(s, el.n)
    u1 = (z * w) % el.n
    u2 = (r * w) % el.n

    x, y = el.point_add(el.scalar_mult(u1, el.g), el.scalar_mult(u2, public_key))

    if (r % el.n) == (x % el.n):
        return 'signature matches'
    else:
        return 'invalid signature'


sock = socket.socket()
sock.connect(('localhost', 9090))
msg = sock.recv(1024)
data = sock.recv(1024).decode()[1:-1].split(")(")
public = literal_eval(data[0])
signature = literal_eval(data[1])

print(verify_signature(public, msg, signature))

