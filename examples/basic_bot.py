from plyable import Plyable

session = Plyable()

while True:
    try:
        in_message = input(">> ")
        print("<< " + session.send(in_message))
    except KeyboardInterrupt:
        break