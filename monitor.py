from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from sys import argv, exit
import time
import pylibmc
import datetime
import socket
import urllib2
import pygerduty
import majsikjul
from carbonfeed import send_to_carbon
from carbonfeed import send_heartbeat_to_carbon

host_name = socket.getfqdn()
pg_api_key = "SECRET_PD_API_KEY"
pager = pygerduty.PagerDuty("allegro-group", "{}".format(pg_api_key))

try:
    script, host, port = argv
except ValueError:
    print("Not enough params")

argscount = len(argv)
if argscount < 3:
    script = argv[0]
    print("you need to tell me fqdn and port")
    print("example usage: {} s13422.dc2 11411").format(script)

    exit(1)

else:
    print("OK, all params passed, let's go.")

key = "1337klucz" + str(host_name)
czas = str((time.time()))
wartoscklucza = (key + czas)

polaczenie = pylibmc.Client(["{}:{}".format(host, port)])
start_set = time.time()
time_stamp = int(start_set)
polaczenie.set(key, wartoscklucza)
end_set = time.time() - start_set

start_get = time.time()
result = polaczenie.get(key)
end_get = time.time() - start_get
end_set_multiplied = end_set * 10

## let's try
polaczenie.delete(key)
##

if wartoscklucza == result:
    print("Keys are equal, everything OK.")
    ismemcacheworking = "yes"
elif wartoscklucza != result:
    print("Something went wrong.")
    ismemcacheworking = "memcacheproblem"
else:
    print("response time for set: %s, response time for get: %s") % (end_set, end_get)

print("Key value: %s, set time: %s, get time: %s" % (result, end_set, end_get))

iswebworking = urllib2.urlopen("http://{}:8091".format(host)).getcode()

if ismemcacheworking == 'yes' and iswebworking == 200:
    print("OK!")
    send_to_carbon(end_set_multiplied)
    print(host_name)
    status = str('ALL OK')
    amiworking = "1"
    majsikjul.tomysql(host_name, end_set, end_get, time_stamp, status)
    send_heartbeat_to_carbon(amiworking)
    print("am i working?: {}".format(amiworking))

    exit(0)
elif ismemcacheworking == 'memcacheproblem':
    status = str(ismemcacheworking)
    majsikjul.tomysql(host_name, end_set, end_get, time_stamp, status)

else:
    print("cos nie dziala")
    print("ismemcacheworking: %s, iswebworking: %s") % (ismemcacheworking, iswebworking)
    status = str(ismemcacheworking) + str(iswebworking)
    pager.trigger_incident("SECRET_PD_API_KEY", "host: {} has some serious problem!".format(host_name),
                           "", "ismemcacheworking: {}, iswebworking: {}".format(ismemcacheworking, iswebworking))
    majsikjul.tomysql(host_name, end_set, end_get, time_stamp, status)
    exit(1)
