#! /usr/bin/python

import pymongo
import pprint
import os

MONGO_PORT = 12717

db = None
drivers = None

def add_driver(args):
    global db, drivers

    driver = {}
    for i in range(len(args)):
        args[i] = args[i].split('=')
        driver[args[i][0]] = args[i][1]

    drivers.insert_one(driver)

def get_driver(args):
    global db, drivers

    driver = {}
    for i in range(len(args)):
        args[i] = args[i].split('=')
        driver[args[i][0]] = args[i][1]

    result = drivers.find_one(driver)

    if (result == None):
        print("Didn't Find")
    else:
        print(result)

def start_client():
    global db, drivers

    # os.system("mongod --dbpath=/data/drivers --port %i" % MONGO_PORT)

    try:
        client = pymongo.MongoClient("mongodb://localhost:%i/" % MONGO_PORT)
    except:
        print("Client Failed to Load")
        return

    db = client["database"]
    drivers = db["drivers"]

class Driver:

    def __init__(self, args):
        self.firstname = args["fname"]
        self.lastname = args["lname"]
        self.gender = args["gender"]
