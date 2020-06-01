import socket
import socketserver
import sys
import requests
import json
import signal
import threading
import time
import os

sys.path.insert(0, "..")

import databases.mongo_client as mongo_client

HOST, PORT = "192.168.0.151", 80

homepage = None
reg_driver_page = None
find_driver_page = None
sign_up_page_html = None
sign_up_page_css = None
sign_up_page_js = None

tcp_server = None

class tcpHandler(socketserver.StreamRequestHandler):

    # point of entry of http tcp request
    def handle(self):
        self.data = self.rfile.readline().strip()
        # print("%s Wrote:" % str(self.client_address))
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

        passed_args = args[1].split("?")

        if args[1] == "/":
            self.wfile.write(bytes(homepage, 'ascii'))
            return

        elif args[1] == "/sign_up.html":
            self.wfile.write(bytes(sign_up_page_html, 'ascii'))

        elif args[1] == "/sign_up.css":
            self.wfile.write(bytes(sign_up_page_css, 'ascii'))

        elif args[1] == "/sign_up.js":
            self.wfile.write(bytes(sign_up_page_js, 'utf-8'))

        elif args[1] == "/register_driver" or args[1] == "/register_driver?":
            self.wfile.write(bytes(reg_driver_page, 'ascii'))
            return

        elif args[1] == "/find_driver" or args[1] == "/find_driver?":
            self.wfile.write(bytes(find_driver_page, 'ascii'))
            return

        elif passed_args[0] == "/register_driver":
            data = passed_args[1].split("&")
            print(data)
            mongo_client.add_driver(data)

        elif passed_args[0] == "/find_driver":
            data = passed_args[1].split("&")
            print(data)
            mongo_client.get_driver(data)

    def process_post(self, args):
        pass

def sigintHandler(sig, frame):
    global tcp_server
    tcp_server.server_close()
    print()
    sys.exit(0)

def reload_html():

    while True:
        global homepage
        global reg_driver_page, find_driver_page
        global sign_up_page_html, sign_up_page_css, sign_up_page_js

        with open("./sign_up/sign_up.html", 'r') as file:
            homepage = file.read()

        with open("./register_driver.html", 'r') as file:
            reg_driver_page = file.read()

        with open("./find_driver.html", 'r') as file:
            find_driver_page = file.read()

        with open("./sign_up/sign_up.html", 'r') as file:
            sign_up_page_html = file.read()

        with open("./sign_up/sign_up.css", 'r') as file:
            sign_up_page_css = file.read()

        with open("./sign_up/sign_up.js", 'r') as file:
            sign_up_page_js = file.read()

        time.sleep(2)

def main():

    signal.signal(signal.SIGINT, sigintHandler)

    r = threading.Thread(target=reload_html, daemon=True)
    r.start()

    mongo_client.start_client()

    global tcp_server
    with socketserver.TCPServer((HOST, PORT), tcpHandler) as tcp_server:
        tcp_server.serve_forever()

if __name__ == "__main__":
    main()
