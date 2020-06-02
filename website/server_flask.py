import socket
import socketserver
import sys
import requests
import json
import signal
import threading
import time
import os

from flask import Flask, render_template, request, redirect

sys.path.insert(0, "..")
import databases.mongo_client as mongo_client

DEBUG = True

app = Flask(__name__)

HOST = "192.168.0.151"
PORT = 80

@app.route("/", methods=["GET", "POST"])
def main_page():

    if request.method == "GET":
        return render_template("sign_up.html")

    elif request.method == "POST":
        pass

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":
        print(request.form)

    else:
        for elem in request.args:
            if request.args[elem] == "":
                return render_template("sign_up.html", invalid_login=1)
        if mongo_client.add_account(request.args):
            return render_template("index.html")

    return render_template("sign_up.html", acc_exists=1)

@app.route("/singin", methods=["GET", "POST"])
def singin():

    if request.method == "POST":
        print(request.form)

    else:
        for elem in request.args:
            if request.args[elem] == "":
                return render_template("sign_up.html", invalid_login=1)
        if (mongo_client.get_account(request.args)):
            return render_template("index.html")

    return render_template("sign_up.html", invalid_login=1)

# SIGNIT HANDLER
def sigintHandler(sig, frame):
    sys.exit(0)

# Reload HTML files for testing
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

# MAIN POINT OF ENTRY
def main():

    signal.signal(signal.SIGINT, sigintHandler)

    # r = threading.Thread(target=reload_html, daemon=True)
    # r.start()

    mongo_client.start_client()

    app.run(HOST, PORT, debug=DEBUG)

if __name__ == "__main__":
    main()
