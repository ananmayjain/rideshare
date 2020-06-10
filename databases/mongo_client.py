#! /usr/bin/python

import pymongo
import pprint
import os
import time
import hashlib
import random
import mail_api

MONGO_PORT = 60000

db = None
valid_accounts = None
account_tokens = None

# Account Verification Email Limit set to 30 minutes
VERIFY_TIME_LIMIT = 30 * 60

def add_account(args):
    global db, valid_accounts, account_tokens
    account = dict(args)

    d = {}
    d["emailid"] = account["emailid"]
    result = valid_accounts.find_one(d)

    if result != None:
        return False

    account["verified"] = False
    valid_accounts.insert_one(account)

    token_d = {}
    token_d["emailid"] = account["emailid"]
    token_d["token"] = hashlib.sha256(str(random.random()).encode()).hexdigest()
    token_d["time"] = round(time.time())

    account_tokens.insert_one(token_d)

    mail_api.sendConfEmail(account["emailid"], token_d["token"])

    return True

def get_account(args):
    global db, valid_accounts

    account = dict(args)

    if valid_accounts.find_one(account) == None:
        return False

    return True

def verify_account(emailid, token):
    global db, valid_accounts, account_tokens

    account = {}
    account["emailid"] = emailid
    account["token"] = token

    result = account_tokens.find_one(account)

    if result == None:
        print("no token")
        return False, False
    elif round(time.time()) - result["time"] > VERIFY_TIME_LIMIT:
        print("time limit")
        return False, True

    account = {}
    account["emailid"] = emailid
    acc_entry = valid_accounts.find_one(account)

    # Sanity Check
    if acc_entry == None:
        print("no valid account entry")
        return False

    valid_accounts.update(account,
        {
            "$set": {"verified": True}
        }
    )

    account_tokens.remove(result)
    return True, True

def start_client():
    global db, valid_accounts, account_tokens

    # os.system("mongod --dbpath=/data/drivers --port %i" % MONGO_PORT)

    try:
        client = pymongo.MongoClient("mongodb://localhost:%i/" % MONGO_PORT)
    except:
        print("Client Failed to Load")
        return

    db = client["database"]
    valid_accounts = db["valid_accounts"]
    account_tokens = db["account_tokens"]

def delete_client(emailid):
    global db, valid_accounts, account_tokens

    account = {}
    account["emailid"] = emailid

    print(valid_accounts.remove(account))
    print(account_tokens.remove(account))

class account:
    def __init__(self, args):
        self.firstname = args["fname"]
        self.lastname = args["lname"]
        self.email = args["email"]
        self.passwd = args["passwd"]
