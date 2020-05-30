import socket
import socketserver
import sys
import requests
import json
import signal

sys.path.insert(0, "..")
# print (sys.path)

# from databases.mongo_client import *

HOST, PORT = "192.168.0.149", 80

# signal.signal(signal.SIGINT, sigintHandler)

with open("index.html", 'r') as file:
    homepage = file.read()

class tcpHandler(socketserver.StreamRequestHandler):

    # point of entry of http tcp request
    def handle(self):
        self.data = self.rfile.readline().strip()
        print("%s Wrote:" % str(self.client_address))
        print (self.data)

        args = self.http_parser(self.data)

        if args[0] == "GET":
            self.process_get(args)
        elif args[1] == "POST":
            self.process_post(args)

    def http_parser(self, data):
        data = data.decode()
        args = data.split(" ")
        return args

    def process_get(self, args):

        if args[1] == "/":
            self.wfile.write(bytes(homepage, 'ascii'))

        elif args[1][0:2] == "/?":
            data = args[1][2:].split("&")
            print(data)


with socketserver.TCPServer((HOST, PORT), tcpHandler) as tcp_server:
    tcp_server.serve_forever()

# def sigintHandler():
#     global tcp_server
#     tcp_server.server_close()
