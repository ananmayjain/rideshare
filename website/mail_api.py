#! /usr/bin/python

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from getpass import getpass
import sys
import hashlib
import random

# PORTS
TSL_PORT = 587
SSL_PORT = 465

# SERVER EMAIL ADDRESS
server_email = "ananmayj8@gmail.com"

# EMAIL TEMPLATES

accountLinkStr = "http://192.168.0.103/confirm_account/"
accountConfTemp = '<p>Please click the link below to activate your account.<br><br><a href=%s>Activate Activate</a><br><br>Thank you,<br>The RideShare Team</p>'

# START THE SERVER
session = smtplib.SMTP(host="smtp.gmail.com", port=TSL_PORT)
session.starttls()

def login_session():

    server_pass = getpass("Enter Email Password: ")

    try:
        session.login(server_email, server_pass)

    except:
        print("LOGIN FAILED")
        session.quit()
        sys.exit(0)

def sendConfEmail(client_email, token):
    msg = MIMEMultipart()
    msg["From"] = "RIDESHARE"
    msg["To"] = client_email
    msg["Subject"] = "Account Confirmation for Rideshare"

    link = accountLinkStr + token + client_email
    body = accountConfTemp % link

    msg.attach(MIMEText(body, "html"))

    session.sendmail(server_email, client_email, msg.as_string())

# sendConfEmail("ananmay.jain@gmail.com", hashlib.sha256(str(random.random()).encode()))
