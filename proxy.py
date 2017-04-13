import socket
import threading
import signal
import sys
import hashlib
import os
import httplib
import urllib2

config = {
    "HOST_NAME": "127.0.0.1",
    "BIND_PORT": 20000,
    "MAX_REQUEST_LEN": 102400,
    "CONNECTION_TIMEOUT": 15
}
flag = 0
blacklisted = ("google", "wikipedia")


class Server:
    def __init__(self, config):
        signal.signal(signal.SIGINT, self.shutdown)  # Shutdown on Ctrl+C
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a TCP socket
        self.serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Re-use the socket
        self.serverSocket.bind(
            (config['HOST_NAME'], config['BIND_PORT']))  # bind the socket to a public host, and a port
        self.serverSocket.listen(10)  # become a server socket
        self.__clients = {}

    def do_GET(self, site_name, port, request):
        print request
        m = hashlib.md5()
        dir_path = os.path.dirname(os.path.realpath(__file__))
        cache_file = site_name.split('.')[0]
        if os.path.exists(cache_file + ".cache"):
            print "Cache hit"
            data = open(cache_file+ ".cache").readlines()
            print data
            return data
        else:
            print "Cache miss"
            req_split = request.split('\r\n')
            http = req_split[0].split(' ')
            # print req_split
            # print http
            term = http[1]
            slash = term.find('0/')
            # print slash
            term = term[slash + 1:]
            # print term
            site = http[1]
            print site
            if 'localhost' in site or '127.0.0' in site:
                ct = 'localhost'
                site = site.split('//')
                site = site[1]
                site = site.split('/')
                site=site[0]
                site = site.split(':')
                site = site[1]
                print site
                port = site
            else:
                site = site.split('//')
                site = site[1]
                site = site.split('/')
                site = site[0]
                site = site.split(':')
                print site
                ct = site[0]
                if len(site) > 1:
                    port  = site[1]
                else:
                    port = 80
            print ct,port
            conn = httplib.HTTPConnection(ct,port)
            conn.request(http[0],term)
            r1 = conn.getresponse()
            print r1.status
            data1 = r1.read()
            # print data1
            # s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # s.settimeout(config['CONNECTION_TIMEOUT'])
            # print site_name, port
            # ip = socket.gethostbyname(site_name)
            # print ip
            # s.connect((ip, port))
            # print 'connect ho gaya'
            # print request


            # http[1] = term
            # print http
            # req_split[0] = ' '.join(http)
            # print req_split
            # del req_split[len(req_split)-1]
            # request = '\n'.join(req_split)
            # print request
            # s.sendall(request)  # send request to webserver
            # data_full = ""
            # print 'going to recv data   '
            # while 1:
            #     data = s.recv(config['MAX_REQUEST_LEN'])  # receive data from web server
            #     print data
            #     open(cache_file + ".cache", 'wb').writelines(data)
            #     data_full += data
            #     break
            return data1
            # m.update(self.path)
            # cache_filename = m.hexdigest() + ".cached"
            # if os.path.exists(cache_filename):
            #   print "Cache hit"
            #   data = open(cache_filename).readlines()
            #   return ("hit", data)
            # else:
            #   print "Cache miss"
            #   data = urllib2.urlopen("http:/" + self.path).readlines()
            #   open(cache_filename, 'wb').writelines(data)
            #   return ("miss", data)
            # return
            # self.send_response(200)
            # self.end_headers()
            # self.wfile.writelines(data)

    def listenForClient(self):
        while True:
            (clientSocket, client_address) = self.serverSocket.accept()  # Establish the connection
            d = threading.Thread(name="Client", target=self.proxy_thread,
                                 args=(clientSocket, client_address))
            d.setDaemon(True)
            d.start()
        self.shutdown(0, 0)

    def proxy_thread(self, conn, client_addr):
        request = conn.recv(config['MAX_REQUEST_LEN'])  # get the request from browser
        # print request
        first_line = request.split('\n')[0]  # parse the first line
        url = first_line.split(' ')[1]  # get url

        # find the webserver and port
        http_pos = url.find("://")  # find pos of ://
        if http_pos == -1:
            temp = url
        else:
            temp = url[(http_pos + 3):]  # get the rest of url

        port_pos = temp.find(":")  # find the port pos (if any)

        # find end of web server
        webserver_pos = temp.find("/")
        if webserver_pos == -1:
            webserver_pos = len(temp)

        webserver = ""
        port = -1
        if port_pos == -1 or webserver_pos < port_pos:  # default port
            port = 80
            webserver = temp[:webserver_pos]
        else:  # specific port
            port = int((temp[(port_pos + 1):])[:webserver_pos - port_pos - 1])
            webserver = temp[:port_pos]

        flag = 0

        try:
            print webserver, port
            # print "Webserver is "
            # print webserver
            for i in range(len(blacklisted)):
                if blacklisted[i] in webserver:
                    flag = 1
            # create a socket to connect to the web server
            # s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # s.settimeout(config['CONNECTION_TIMEOUT'])
            # if flag is 0:
            #     s.connect((webserver, port))
            #     s.sendall(request)  # send request to webserver
            #
            # if flag is 0:
            #     while 1:
            #         data = s.recv(config['MAX_REQUEST_LEN'])  # receive data from web server
            #         if len(data) > 0:
            #             conn.send(data)  # send to browser
            #         else:
            #             break
            data = self.do_GET(webserver, port, request)
            print 'Sending to client \n', data
            # str1 =
            conn.send(data)

        except socket.error as error_msg:
            print 'ERROR: ', client_addr, error_msg
        if conn:
            conn.close()

    def _getClientName(self, cli_addr):
        """ Return the clientName.
        """
        return "Client"

    def shutdown(self, signum, frame):
        """ Handle the exiting server. Clean all traces """
        self.serverSocket.close()
        sys.exit(0)


if __name__ == "__main__":
    server = Server(config)
    server.listenForClient()
