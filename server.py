import socket
import random
import elliptic_module as el

sock = socket.socket()
sock.bind(('', 9090))
sock.listen(1)
conn, addr = sock.accept()


def make_keypair():
    private_key = random.randrange(1, el.n)
    public_key = el.scalar_mult(private_key, el.g)

    return private_key, public_key


def sign_message(private_key, message):
    z = el.hash_message(message)

    r = 0
    s = 0

    while not r or not s:
        k = random.randrange(1, el.n)
        x, y = el.scalar_mult(k, el.g)

        r = x % el.n
        s = ((z + r * private_key) * el.inverse_mod(k, el.n)) % el.n

    return (r, s)


private, public = make_keypair()
print("Private key:", private)
print("Public key:", public)

msg = b'Hello!'
signature = sign_message(private, msg)
print(signature)

conn.send(msg)
conn.send(str(public).encode() + str(signature).encode())
