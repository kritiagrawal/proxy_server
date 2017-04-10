import os
import sys
import random
import time

if len(sys.argv) < 4:
    print "Usage: python client.py <CLIENT_PORTS_RANGE> <PROXY_PORT> <END_SERVER_PORT>"
    print "Example: python client.py 19990-19999 20000 20010"
    raise SystemExit

CLIENT_PORT = sys.argv[1]
PROXY_PORT = sys.argv[2]
SERVER_PORT = sys.argv[3]

D = {0: "GET", 1: "GET"}

while True:
    filename = "%d.data" % (int(random.random() * 2) + 1)
    METHOD = D[int(random.random() * len(D))]
    CLIENT_PORT = str(random.randint(int(CLIENT_PORT), int(CLIENT_PORT) + 6))

    print 'sending request - ', "curl --request GET --proxy 127.0.0.1:%s --local-port %s geeksforgeeks.org" % (
        PROXY_PORT, CLIENT_PORT)

    os.system("curl --request GET --proxy 127.0.0.1:%s geeksforgeeks.org" % (
        PROXY_PORT))

    time.sleep(5)

    print 'sending request - ', "curl --request %s --proxy 127.0.0.1:%s --local-port %s 127.0.0.1:%s/%s" % (
        METHOD, PROXY_PORT, CLIENT_PORT, SERVER_PORT, filename)

    os.system("curl --request %s --local-port %s 127.0.0.1:%s/%s" % (
        METHOD, CLIENT_PORT, SERVER_PORT, filename))

    time.sleep(10)
