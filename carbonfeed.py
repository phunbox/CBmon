import socket
import time
def send_to_carbon(end_set_multiplied):
    hostname = socket.gethostname()
    sock = socket.socket()
    timestamp = int(time.time())

    sock.connect(("skystats.qxlint", 2003))
    sock.send("stats.tech.5cache.%s.set_test %r %d\n" % (hostname, end_set_multiplied, timestamp))
    sock.close()

def send_heartbeat_to_carbon(amiworking):
    hostname = socket.gethostname()
    sock = socket.socket()
    timestamp = int(time.time())

    sock.connect(("skystats.qxlint", 2003))
    sock.send("stats.tech.5cache.%s.is_working %s %d\n" % (hostname, amiworking, timestamp))
    sock.close()

