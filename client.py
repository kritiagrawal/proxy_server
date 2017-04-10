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

D = {0: "GET", 1: "POST"}

while True:
    filename = "%d.data" % (int(random.random() * 9) + 1)
    METHOD = D[int(random.random() * len(D))]
    print 'sending request - ', "curl --request GET --proxy 127.0.0.1:%s --local-port %s geeksforgeeks.org" % (
         PROXY_PORT, CLIENT_PORT)
    os.system("curl --request GET --proxy 127.0.0.1:%s geeksforgeeks.org" % (
        PROXY_PORT))
    time.sleep(10)
