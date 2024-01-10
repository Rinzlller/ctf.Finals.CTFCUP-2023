#!/usr/bin/env python3

import grpc
from oilmarket_pb2 import *
from oilmarket_pb2_grpc import OilmarketStub

# example generating: 
# python -m grpc_tools.protoc -I../../protos --python_out=. --pyi_out=. --grpc_python_out=. ../../protos/helloworld_77.proto
# here need to import contracts

import random
import string
import re
import sys
import json


port = 2112
flag_regexp = re.compile(r'[A-Z0-9]{31}=')


class Standart_User:
    def __init__(self, ip):

        # gRPC vars
        self.insecure_channel = grpc.insecure_channel(f"{ip}:{port}")
        self.stube = OilmarketStub(self.insecure_channel)

        # User vars
        random_string = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(8))
        self.flag = f"{''.join(random.choice(string.ascii_letters + string.digits).upper() for _ in range(31))}="
        self.name = random_string

        # AutoStart
        self.create_attester()
        self.create_buyer()


    def create_attester(self):
        resp = self.stube.CreateAttester(CreateAttesterRequest(
                name = self.name
        ))
        return resp


    def create_buyer(self):
        resp = self.stube.CreateBuyer(CreateBuyerRequest(
                name = self.name,
                flag = self.flag,
                attesters = [
                    self.name
                ]
        ))
        return resp
        
    
def main():

    try:
        ip = sys.argv[1]
    except:
        print(f"USAGE:\t{sys.argv[0]} <victim-ip-address>")
        sys.exit(1)

    ip = sys.argv[1]

    for _ in range(5):
        normal_m0th3rfuck3r = Standart_User(ip)
        print( normal_m0th3rfuck3r.name )
    

if __name__ == "__main__":  
    main()
        