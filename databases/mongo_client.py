#! /usr/bin/python

import pymongo
import pprint
import os

MONGO_PORT = 60000

db = None
valid_accounts = None

def add_account(args):
    global db, valid_accounts
    account = dict(args)

    test_d = {}
    test_d["emailid"] = account["emailid"]
    result = valid_accounts.find_one(test_d)

    if result != None:
        return False

    valid_accounts.insert_one(account)

    return True

def get_account(args):
    global db, valid_accounts

    account = dict(args)

    if valid_accounts.find_one(account) == None:
        return False

    return True

def start_client():
    global db, valid_accounts

    # os.system("mongod --dbpath=/data/drivers --port %i" % MONGO_PORT)

    try:
        client = pymongo.MongoClient("mongodb://localhost:%i/" % MONGO_PORT)
    except:
        print("Client Failed to Load")
        return

    db = client["database"]
    valid_accounts = db["valid_accounts"]

class account:
    def __init__(self, args):
        self.firstname = args["fname"]
        self.lastname = args["lname"]
        self.email = args["email"]
        self.passwd = args["passwd"]
